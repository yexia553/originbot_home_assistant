<template>
    <div class="voice-control">
        <div style="position: fixed; bottom: 30%; left: 50%;">
            <el-button type="primary" circle :class="{ 'is-recording': isRecording }" @mousedown="startRecording"
                @mouseup="stopAndSend"
                style="transform: translate(-50%, -50%); cursor: pointer; width: 4vw; height: 4vw; line-height: 4vw;">
                <el-icon size='35'>
                    <Microphone />
                </el-icon>
            </el-button>
        </div>
    </div>
</template>

<script>
import { ref } from "vue";
import axios from "axios";
import Recorder from 'recorder-core';
import 'recorder-core/src/engine/wav';

export default {
    setup() {
        const isRecording = ref(false);
        let recorder = null;

        const startRecording = () => {
            console.log("开始录音...");
            isRecording.value = true;

            recorder = Recorder({
                type: "wav",
                sampleRate: 16000,
                bitRate: 16,
            });
            recorder.open(() => {
                console.log("录音已打开");
                recorder.start()
            }, (msg, isUserNotAllow) => {
                //用户拒绝了录音权限，或者浏览器不支持录音
                console.log((isUserNotAllow ? "UserNotAllow，" : "") + "无法录音:" + msg);
            })
        };

        const stopAndSend = () => {
            if (recorder) {
                recorder.stop((blob, duration) => {
                    console.log("停止录音...");
                    isRecording.value = false;

                    // 发送录音数据到后端
                    let formData = new FormData();
                    formData.append('audio_file', blob, 'recording.wav');
                    console.log("准备发送数据");
                    axios.post('http://localhost:8000/api/voice_control/', formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    }).then(response => {
                        console.log(response.data);
                    }).catch(error => {
                        console.error(error);
                    });
                }, msg => {
                    console.error(msg);
                });
            }
        };

        return {
            startRecording,
            stopAndSend,
            isRecording
        };
    },
}
</script>

<style scoped>
.is-recording {
    transform: scale(1.05);
    transition: transform 0.3s ease-in-out;
}

body {
    background-color: #212529;
}
</style>
