import React, { useRef, useEffect} from 'react';
import * as cv from 'opencv-ts';

function App() {

  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  
  useEffect(() => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    navigator.mediaDevices.enumerateDevices()
    .then((devices) => {
      const cameras = devices.filter((device) => device.kind === 'videoinput');
      const cameraId = cameras[2].deviceId;
      
      return navigator.mediaDevices.getUserMedia({ video: {deviceId: {exact: cameraId } } });
    })
    
    .then((stream) => {
      video.srcObject = stream;
      video.play();
      
      const processVideo = () => {
        const { videoWidth, videoHeight } = video;
        
        canvas.width = videoWidth;
        canvas.height = videoHeight;
        
        ctx.drawImage(video, 0, 0, videoWidth, videoHeight);
        
        const srcMat = cv.imread(canvas);
        
        cv.imshow(canvas, srcMat);
        
        srcMat.delete();
        
        requestAnimationFrame(processVideo);
};

processVideo();
})
.catch((err) => {
  console.error('Error accessing camera', err);
});
}, []);

return (
<div className="video-container">
<video ref={videoRef} />
//<canvas ref={canvasRef} />
</div>
);
}

export default App;
