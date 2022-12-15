import cv2 
import numpy as np
from imutils.perspective import four_point_transform

def imshowSmall(window, img):
    cv2.imshow(window, cv2.resize(img, None, fx=0.25, fy=0.25, interpolation =cv2.INTER_AREA))

def simplifyContour(contour, cornerCount=4):
    """
    Tries to find epsilon such that new simplified contour have specified corner count,
    returns unchanged contour on fail, else simplified contour 
    """
    i, maxIterations = 0, 100
    lowerBound, upperBound = 0., 1.
    perimeter = cv2.arcLength(contour, closed=True)
    
    while True:
        i+=1
        if i > maxIterations:
            return contour
        
        k = (lowerBound+upperBound)/2
        eps = k * perimeter
        approx = cv2.approxPolyDP(contour, eps, closed= True)
        if len(approx) > cornerCount: 
            lowerBound = (lowerBound+upperBound)/2.0
        elif len(approx) < cornerCount:
            upperBound = (lowerBound+upperBound)/2.0
        else:
            return approx

def parallelizeDocumentContour(contour): 
    """
    Makes quadrilateral contour have parallel sides, so it's not squished under transform
    """
    topBound = min(contour[0,0,1], contour[3,0,1])
    contour[0,0,1], contour[3,0,1] = topBound, topBound
    bottomBound = min(contour[1,0,1], contour[2,0,1])
    contour[1,0,1], contour[2,0,1] = bottomBound, bottomBound
    return contour 


def findDocumentContour(img):
    """
    Finds contour of a scanned document, returns contour and thresholded image
    """
    height, width = img.shape[:2]
    #base contour - full image
    document_contour = np.array([[0,0], [width, 0], [width, height], [0, height]], dtype=np.int32)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #blur to remove the noise for thresholding
    imgBlur = cv2.GaussianBlur(imgGray, (5,5), 0)
    #calculates threshold of image using Otsu method
    _, threshold = cv2.threshold(imgBlur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # threshold = cv2.erode(threshold, np.ones((5,5), np.uint8))

    #contours are lists of points that make a contour
    contours, _ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #contours sorted by their area
    contoursSorted = sorted(contours, key=cv2.contourArea, reverse=True)

    for contour in contoursSorted:
        area = cv2.contourArea(contour)
        if area > 1000:
            #perimeter of closed contour
            perimeter= cv2.arcLength(contour, True)
            #calculating approximated contour
            approxContour = cv2.approxPolyDP(curve=contour, epsilon=0.02 * perimeter, closed= True)
            if len(approxContour) > 4:
                #if contour is not simplified enough we try to bissect epsilon till it is
                newApproxContour = simplifyContour(approxContour)
                if len(newApproxContour) > 4:
                    continue
                else:
                    document_contour = newApproxContour
                    break
            elif len(approxContour) == 4:
                document_contour = approxContour
                break
    return (document_contour, threshold)

img = cv2.imread("receipt.png")

while True:
    img_copy = img.copy()

    documentContour, imgThreshold = findDocumentContour(img_copy)
    # documentContour = parallelizeDocumentContour(documentContour)
    imgThreshold = cv2.drawContours(cv2.cvtColor(imgThreshold, cv2.COLOR_GRAY2BGR), [documentContour], -1, (0,255,0), 3)
    imshowSmall("Contour", imgThreshold)
    
    imgWarped = four_point_transform(img_copy, documentContour.reshape(4,2))
    imshowSmall("Warped", imgWarped)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()

