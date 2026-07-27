const { app, BrowserWindow } = require("electron");
const path = require("path");


function createWindow(){

    const win = new BrowserWindow({

        width:1200,
        height:800,

        webPreferences:{
            nodeIntegration:true,
            contextIsolation:true,
            preload: path.join(__dirname, "preload.js")
        }

    });


    win.loadFile(
        "../frontend/index.html"
    );

}


app.whenReady().then(createWindow);


app.on(
    "window-all-closed",
    ()=>{
        if(process.platform !== "darwin"){
            app.quit();
        }
    }
);