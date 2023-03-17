const cv = require('opencv-ts');

// Get the video element from the HTML page
const video = document.getElementById('camera');
const video2 = document.getElementById('camera2');
const video3 = document.getElementById('camera3');

// Create a new video capture object with the camera index (0 for the first camera)
const cap1 = new cv.VideoCapture(4);
const cap2 = new cv.VideoCapture(2);
const cap3 = new cv.VideoCapture(4);

// Set the camera resolution
cap1.set(cv.CAP_PROP_FRAME_WIDTH, 640);
cap1.set(cv.CAP_PROP_FRAME_HEIGHT, 480);
cap2.set(cv.CAP_PROP_FRAME_WIDTH, 640);
cap2.set(cv.CAP_PROP_FRAME_HEIGHT, 480);
cap3.set(cv.CAP_PROP_FRAME_WIDTH, 640);
cap3.set(cv.CAP_PROP_FRAME_HEIGHT, 480);

// Start the video capture
cap1.readAsync((err, frame) => {
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
}
);

cap2.readAsync((err, frame) => {
    if (!err) {
      // Display the frame in the video element
      cv.imshow(video2, frame);
  
      // Repeat the process for the next frame
      setTimeout(() => cap2.readAsync((err, frame) => {
        if (!err) {
          cv.imshow(video2, frame);
          setTimeout(arguments.callee, 0);
        }
      }), 0);
    }
  }
);

  cap3.readAsync((err, frame) => {
    if (!err) {
      // Display the frame in the video element
      cv.imshow(video3, frame);
  
      // Repeat the process for the next frame
      setTimeout(() => cap3.readAsync((err, frame) => {
        if (!err) {
          cv.imshow(video3, frame);
          setTimeout(arguments.callee, 0);
        }
      }), 0);
    }
  }
  );



