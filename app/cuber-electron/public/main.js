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
            contextIsolation: false
        }
    })

    win.loadURL(
 'http://localhost:3000'
        )
}

app.on('ready', createWindow)