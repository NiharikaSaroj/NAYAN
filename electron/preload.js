const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld(
    "electronAPI",
    {

        appName: "NAYAN",

        version: "1.0",

        testMic: async () => {

            try {

                const stream = await navigator.mediaDevices.getUserMedia({
                    audio: true
                });

                stream.getTracks().forEach(track => track.stop());

                return "Microphone access granted";

            } catch (error) {

                return "Microphone access denied: " + error.message;

            }

        },

        startVoiceChat: () =>
            ipcRenderer.invoke("start-voice-chat"),

        speakText: (text) =>
            ipcRenderer.invoke("speak-text", text),

        onVoiceMessage(callback) {

            ipcRenderer.on(
                "voice-message",
                (event, data) => callback(data)
            );

        }

    }
);