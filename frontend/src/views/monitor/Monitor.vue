<template>
    <div>
        <div class="VideoPlayer">
            <video ref="videoPlayer" class="video-js vjs-default-skin" controls></video>
        </div>
    </div>
</template>

<script>
import { onMounted, onBeforeUnmount, ref, getCurrentInstance } from 'vue';
import videojs from 'video.js'
import 'video.js/dist/video-js.css'

export default {
    name: 'VideoPlayer',
    setup() {
        const videoPlayer = ref(null);
        const videoUrl = ref('');
        let player;

        const { proxy } = getCurrentInstance()

        onMounted(async () => {
            let res = await proxy.$api.getRTMPToken();
            if (res.status === 200) {
                console.log(res.data)
                const username = res.data.results[0].username;
                const password = res.data.results[0].password;
                videoUrl.value = `http://${username}:${password}@10.11.12.173:8001/hls/babycare.m3u8`
                console.log(videoUrl)

                player = videojs(videoPlayer.value, {}, () => {
                    console.log('Player ready')
                    player.src({
                        src: videoUrl.value,
                        type: 'application/x-mpegURL', // Or other relevant type depending on the stream
                    })
                    player.play();
                });

            } else {
                console.error('Failed to get rtmp token');
            }
        });

        onBeforeUnmount(() => {
            if (player) {
                player.dispose();
            }
        });

        return {
            videoUrl,
            videoPlayer
        };
    },
}
</script>

<style scoped>
.video-js {
    width: 640px;
    height: 480px;
}
</style>
