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

                    win.webContents.send(
                        "voice-message",
                        {
                            role: "state",
                            text: line.replace(
                                "UI_STATE::",
                                ""
                            )
                        }
                    );

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

        }
    );

}

function createWindow() {

    win = new BrowserWindow({

        width: 1200,
        height: 800,

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

}

app.whenReady().then(createWindow);

app.on(
    "window-all-closed",
    () => {

        if (voiceProcess) {
            voiceProcess.kill();
        }

        if (process.platform !== "darwin") {
            app.quit();
        }

    }
);
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