import numpy as np
import pytesseract
import cv2
from imutils.perspective import four_point_transform
import re

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
    threshold = cv2.erode(threshold, np.ones((3,3), np.uint8))

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

def scan(image):
    img = cv2.imread(image)

    documentContour, imgThreshold = findDocumentContour(img)
    # imgThreshold = cv2.drawContours(cv2.cvtColor(imgThreshold, cv2.COLOR_GRAY2BGR), [documentContour], -1, (0,255,0), 3)
    
    # cv2.imwrite("/server/receiptImages/img.png", imgThreshold) #printing threshold image
    
    imgWarped = four_point_transform(img, documentContour.reshape(4,2))
    
    # cv2.imwrite("/server/receiptImages/imgWar.png", imgWarped) # printing cut out image
    
    options = "--psm 6"
    data = pytesseract.image_to_string(cv2.cvtColor(imgWarped, cv2.COLOR_BGR2RGB), lang='pol', config=options)
    
    company_name = data.split("\n")[0]
    
    # \b is a word boundary. It matches the beginning and ending of a word
    addressRegex = r'(\b[0-9]{2}\-[0-9]{3}\b)'
    address = None 
    
    # two formats of saving data on the receipts
    dateRegex = r'(\b[0-9]{2}\-[0-9]{2}\-[0-9]{4}\b|\b[0-9]{4}\-[0-9]{2}\-[0-9]{2}\b)'
    date = None 
    
    priceRegex = r'(\b[0-9]+(\,|\.)[0-9]{2}\b)'
    items = None

    total_value = None
    debug = []

    for row in data.split("\n"):
        if re.search(addressRegex, row) is not None:
            address = row
        if re.search(dateRegex, row) is not None:
            try:
                date = re.search(addressRegex, row).group(1) # taking only the date out of the date row
            except Exception as e:
                continue
           
        # Searching for total value
        suma_list = ['SUMA', 'Suma', 'SUMA PLN', 'SUMA: PLN']
        if any(suma in row for suma in suma_list):
            # total_index = data.index('SUMA')
            # total_value = data[total_index + 8].replace(',', '.')
            try:
                total_value = re.search(priceRegex, row).group(1)
            except Exception as e:
                continue
            
        # Looking for rows containing prices
        match = re.search(priceRegex, row)
        if match:
            items = [] if items == None else items
            words = row.split()
            print(row, words, match, match.group())
            try:
                price_index = words.index(match.group())
            except ValueError as e:
                continue

            description = ' '.join(words[:price_index])
            price = match.group()[1:].replace(',', '.')
            items.append({'description': description, 'price': price})
            
    # Uncomment if you want to see all of the lines and comment next context inicialization
    #     debug.append(row)
    # context = {'company': company_name, 'address': address, 'date': date, 'full_price': total_value, 'items': items, 'debug': debug}
            
    context = {'company': company_name, 'address': address, 'date': date, 'full_price': total_value, 'items': items}

    return context, imgThreshold