import React from 'react';
import './App.css';
import rubiksGif from './ImageComponents/rubiksGif.gif';
import { useEffect, useRef } from 'react';


function App() {

  const titleLetters = [
    { letter: 'R', color: 'lime' },
    { letter: 'u', color: 'white' },
    { letter: 'b', color: 'turquoise' },
    { letter: 'i', color: 'orange' },
    { letter: 'k', color: 'yellow' },
    { letter: `'`, color: 'red'},
    { letter: 's', color: 'red' },
    { letter: `.`, color: '#333' },
    { letter: 'C', color: 'lime' },
    { letter: 'u', color: 'white' },
    { letter: 'b', color: 'turquoise' },
    { letter: 'e', color: 'orange' },
    { letter: '.', color: '#333' },
    { letter: 'S', color: 'lime' },
    { letter: 'o', color: 'white' },
    { letter: 'l', color: 'turquoise' },
    { letter: 'v', color: 'orange' },
    { letter: 'e', color: 'yellow' },
    { letter: 'r', color: 'red' },
  ];

  const videoRef = useRef("camera-feed");

  useEffect(() => {
    // Get the camera stream and display it in a video element
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        const video = videoRef.current;
        video.srcObject = stream;
        video.play();
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
              {titleLetters.map((letter, index) => (
          <span key={index} style={{ color: letter.color }}>{letter.letter}</span>
        ))}
      </header>
      <div className="App-container">
         <div className="left-menu">
           <button className="menu-button">Home</button>
           <button className="menu-button">Live View</button>
           <button className="menu-button">Scramble Function</button>
          <button className="menu-button">Solve Cube</button>
         </div>
         <div className="App-body">
           <main className="App-main">
           <div className="gif-container">
    <img src={rubiksGif} alt="gif of a rotating rubiks cube" className="centered-gif" />
  </div>
           <h1>How to Use the Rubik's Cube Solver</h1>
  <p>
    The Rubik's Cube Solver is a powerful tool that can help you solve any scrambled Rubik's Cube in just a few minutes. To use the solver, simply follow these steps:
  </p>
  <ol>
    <li>Enter the colors of your scrambled Rubik's Cube into the input fields on the solver page.</li>
    <li>Click the "Solve" button to run the solver algorithm.</li>
    <li>The solver will show you a step-by-step solution for solving your Rubik's Cube.</li>
  </ol>
  <p>
    With the Rubik's Cube Solver, you'll never have to spend hours trying to solve your Rubik's Cube again. Give it a try today and see how easy it is to solve your cube!
  </p>
        </main>
         </div>
       </div>
       <div className="video-container">
       <video ref={videoRef} autoPlay muted></video>      
       </div>
    </div>
  );
}

export default App;


