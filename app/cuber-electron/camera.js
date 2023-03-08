const cv = require('opencv-ts');

// Get the video element from the HTML page
const video = document.getElementById('camera');

// Create a new video capture object with the camera index (0 for the first camera)
const cap = new cv.VideoCapture(0);

// Set the camera resolution
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640);
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480);

// Start the video capture
cap.readAsync((err, frame) => {
  if (!err) {
    // Display the frame in the video element
    cv.imshow(video, frame);

    // Repeat the process for the next frame
    setTimeout(() => cap.readAsync((err, frame) => {
      if (!err) {
        cv.imshow(video, frame);
        setTimeout(arguments.callee, 0);
      }
    }), 0);
  }
});
