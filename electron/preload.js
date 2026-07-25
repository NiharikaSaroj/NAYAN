const { contextBridge } = require("electron");


contextBridge.exposeInMainWorld(
    "electronAPI",
    {

        appName:"NAYAN",

        version:"1.0"

    }
);