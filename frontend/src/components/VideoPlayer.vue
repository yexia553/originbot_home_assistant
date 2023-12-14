<template>
    <div class="VideoPlayer">
        <video ref="videoPlayer" class="vjs-default-skin" controls autoplay></video>
    </div>
</template>

<script>
import { onMounted, onBeforeUnmount, ref } from 'vue';

export default {
    name: 'VideoPlayer',
    props: ['url'],
    setup(props) {
        const videoPlayer = ref(null);
        let mediaSource = new MediaSource();
        let sourceBuffer;
        let socket;

        onMounted(() => {
            videoPlayer.value.src = URL.createObjectURL(mediaSource);
            mediaSource.addEventListener('sourceopen', sourceOpen);

            socket = new WebSocket(props.url);
            socket.binaryType = 'arraybuffer';
            socket.onmessage = (event) => {
                if (sourceBuffer && !sourceBuffer.updating) {
                    sourceBuffer.appendBuffer(event.data);
                }
            };
        });

        function sourceOpen(event) {
            sourceBuffer = mediaSource.addSourceBuffer('video/mp4; codecs="avc1.64001E, mp4a.40.2"');
        }

        onBeforeUnmount(() => {
            if (socket) {
                socket.close();
            }
            if (mediaSource) {
                mediaSource.endOfStream();
            }
        });

        return {
            videoPlayer
        };
    },
}
</script>

<style scoped>
.video-js {
    width: 640px;
    height: 360px;
}
</style>
