// function clearPhoto(photo, canvas) {
//   const ctx = canvas.getContext("2d");
//   ctx.fillStyle = "#AAA";
//   ctx.fillRect(0, 0, canvas.width, canvas.height);
//   const data = canvas.toDataURL("image/png");
//   photo.setAttribute("src", data);
// }

function takePhoto(photo, canvas, video, width, height) {
  const ctx = canvas.getContext("2d");
  canvas.width = width;
  canvas.height = height;
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  const data = canvas.toDataURL("image/png");
  photo.setAttribute("src", data);

  canvas.toBlob(function (blob) {
    const file = new File([blob], "receipt.png", { type: "image/png" });
    let container = new DataTransfer();
    container.items.add(file);
    const imageUploader = document.getElementById("id_receipt_image");
    imageUploader.files = container.files;
  }, "image/png");
  
  document.getElementById("take-photo-button").style.display = "flex";
}

(main = async () => {
  const videoPhotoSection = document.getElementById("webcam-photo");
  const video = document.getElementById("webcam");
  const photo = document.getElementById("photo");
  const canvas = document.getElementById("canvas");
  const takePhotoButton = document.getElementById("take-photo-button");
  const videoSize = { width: 1920, height: 1080 };
  const videoConstraints = {
    audio: false,
    video: videoSize,
  };
  let stream = null;
  videoPhotoSection.style.display = "None";
    try {
    stream = await navigator.mediaDevices.getUserMedia(videoConstraints);
  } catch(err) {
    console.error(`${err.name}: ${err.message}`);
    return null;
  }
  video.srcObject = stream;
  video.onloadedmetadata = () => {
    video.play();
  };
  takePhotoButton.addEventListener(
    "click",
    (e) => {
      takePhoto(photo, canvas, video, videoSize.width, videoSize.height);
      e.preventDefault();
    },
    false
  );

  //   clearPhoto(photo, canvas);
})();
