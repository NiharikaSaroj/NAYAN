const { app, BrowserWindow } = require("electron");
const path = require("path");
const { spawn } = require("child_process");

const wakeMode = process.argv.includes("--wake");
const { ipcMain } = require("electron");

let voiceProcess;
let win;

function startVoiceEngine() {

    const pythonPath = path.join(
        __dirname,
        "../voice_engine/venv/Scripts/python.exe"
    );

    const voiceScript = path.join(
        __dirname,
        "../voice_engine/main.py"
    );

    voiceProcess = spawn(
        pythonPath,
        [voiceScript],
        {
            windowsHide: true
        }
    );

    // Listen for output from voice engine
    voiceProcess.stdout.on(
        "data",
        (data) => {

            const output = data.toString();

            console.log(output);

            output.split("\n").forEach(line => {

                line = line.trim();

                if (!line) return;

                // User message
                if (line.startsWith("UI_USER::")) {

                    win.webContents.send(
                        "voice-message",
                        {
                            role: "user",
                            text: line.replace(
                                "UI_USER::",
                                ""
                            )
                        }
                    );

                }

                // AI message
                else if (line.startsWith("UI_AI::")) {

                    win.webContents.send(
                        "voice-message",
                        {
                            role: "assistant",
                            text: line.replace(
                                "UI_AI::",
                                ""
                            )
                        }
                    );

                }

                // UI state
                else if (line.startsWith("UI_STATE::")) {

                    const state = line.replace("UI_STATE::", "").trim();

                    console.log("STATE FROM PYTHON:", state);

                    win.webContents.send(
                        "voice-message",
                        {
                            role: "state",
                            text: state
                        }
                    );

                    // Python is asking Electron to close
                    if (state === "shutdown") {

                        console.log("Shutdown requested by voice engine");

                        if (voiceProcess) {
                            voiceProcess.kill();
                            voiceProcess = null;
                        }

                        if (win && !win.isDestroyed()) {
                            win.close();
                        }
                    }

                }

                // Normal debug output
                else {

                    console.log("VOICE:", line);

                }

            });

        }
    );

    voiceProcess.stderr.on(
        "data",
        (data) => {

            console.error(
                "VOICE ERROR:",
                data.toString()
            );

        }
    );

    voiceProcess.on(
        "close",
        (code) => {

            console.log(
                `Voice engine stopped with code ${code}`
            );

            voiceProcess = null;

        }
    );

}

function createWindow() {

    win = new BrowserWindow({

        width: 1400,
        height: 900,
        show: false,

        webPreferences: {

            nodeIntegration: true,
            contextIsolation: true,

            preload: path.join(
                __dirname,
                "preload.js"
            )

        }

    });

    if (wakeMode) {

        win.loadFile(
            "../frontend/chat.html"
        );

        // Start voice engine only in wake mode
        startVoiceEngine();

    }
    else {

        win.loadFile(
            "../frontend/index.html"
        );

    }
    win.maximize();

    win.show();

    win.focus();

}

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {

    console.log("Electron window closed");

    if (voiceProcess) {
        voiceProcess.kill();
        voiceProcess = null;
    }

    app.quit();

});
ipcMain.handle(
    "start-voice-chat",
    async () => {

        return new Promise((resolve) => {

            const pythonPath = path.join(
                __dirname,
                "../voice_engine/venv/Scripts/python.exe"
            );

            const script = path.join(
                __dirname,
                "../voice_engine/voice_chat.py"
            );

            const process = spawn(
                pythonPath,
                [script],
                {
                    windowsHide: true
                }
            );

            process.stdout.on(
                "data",
                (data) => {

                    const output = data.toString();

                    console.log(output);

                    output.split("\n").forEach(line => {

                        line = line.trim();

                        if (!line) return;

                        if (line.startsWith("UI_USER::")) {

                            win.webContents.send(
                                "voice-message",
                                {
                                    role: "user",
                                    text: line.replace("UI_USER::", "")
                                }
                            );

                        }

                        else if (line.startsWith("UI_AI::")) {

                            win.webContents.send(
                                "voice-message",
                                {
                                    role: "assistant",
                                    text: line.replace("UI_AI::", "")
                                }
                            );

                        }

                        else if (line.startsWith("UI_STATE::")) {

                            win.webContents.send(
                                "voice-message",
                                {
                                    role: "state",
                                    text: line.replace("UI_STATE::", "")
                                }
                            );

                        }

                    });

                }
            );

            process.on(
                "close",
                () => resolve(true)
            );

        });

    }
);

ipcMain.handle(
    "speak-text",
    async (event, text) => {

        return new Promise((resolve) => {

            console.log("Speak requested:", text);

            win.webContents.send(
                "voice-message",
                {
                    role: "state",
                    text: "speaking"
                }
            );

            const pythonPath = path.join(
                __dirname,
                "../voice_engine/venv/Scripts/python.exe"
            );

            console.log("Python:", pythonPath);

            const script = path.join(
                __dirname,
                "../voice_engine/speak.py"
            );

            console.log("Script:", script);

            const process = spawn(
                pythonPath,
                [script, text],
                {
                    windowsHide: true
                }
            );

            process.stdout.on("data", (data) => {
                console.log("SPEAK:", data.toString());
            });

            process.stderr.on("data", (data) => {
                console.error("SPEAK ERROR:", data.toString());
            });

            process.on(
                "close",
                (code) => {

                    console.log("Speak process exited:", code);

                    win.webContents.send(
                        "voice-message",
                        {
                            role: "state",
                            text: "idle"
                        }
                    );

                    resolve(true);

                }
            );

        });

    }
);