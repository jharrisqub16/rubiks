const { app, BrowserWindow } = require('electron') //634 (gzipped: 392)

const path = require('path')
// const isDev = require('electron-is-dev')

require('@electron/remote/main').initialize() 


function createWindow() {
    //Create the browser window.

    const win = new BrowserWindow({
        width: 800,
        height: 600, 
        webPreferences: {
            nodeIntegration: true,
            enableRemoteModule: true,
            contextIsolation: false,
            webSecurity: false
        }
    })

    win.loadURL(
 'http://localhost:3000'
        )

          // Get the camera stream and display it in a video element
          win.webContents.on('did-finish-load', () => {
            win.webContents.executeJavaScript(`
  navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    const video = document.createElement('video');
    video.setAttribute('id', 'camera');
    video.setAttribute('class', 'camera-feed');
    video.setAttribute('autoplay', '');
    video.srcObject = stream;
    document.body.appendChild(video);
  })
  .catch(error => {
    console.error(error);
  });
  `)
  win.webContents.executeJavaScript(`
  navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    const video = document.createElement('video2');
    video.setAttribute('id', 'camera2');
    video.setAttribute('class', 'camera-feed2');
    video.setAttribute('autoplay', '');
    video.srcObject = stream;
    document.body.appendChild(video);
  })
  .catch(error => {
    console.error(error);
  });
  `)
  win.webContents.executeJavaScript(`
  navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    const video = document.createElement('video3');
    video.setAttribute('id', 'camera3');
    video.setAttribute('class', 'camera-feed3');
    video.setAttribute('autoplay', '');
    video.srcObject = stream;
    document.body.appendChild(video);
  })
  .catch(error => {
    console.error(error);
  });
  `)
})
}

app.on('ready', createWindow)