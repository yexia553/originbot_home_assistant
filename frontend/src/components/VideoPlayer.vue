<template>
    <div class="VideoPlayer">
        <video ref="videoPlayer" class="video-js vjs-default-skin" controls></video>
    </div>
</template>

<script>
import { onMounted, onBeforeUnmount, ref } from 'vue';
import videojs from 'video.js'
import 'video.js/dist/video-js.css'

export default {
    name: 'VideoPlayer',
    props: ['url'],
    setup(props) {
        const videoPlayer = ref(null);
        let player;

        onMounted(() => {
            player = videojs(videoPlayer.value, {}, () => {
                console.log('Player ready')
                player.src({
                    src: props.url,
                    type: 'application/x-mpegURL', // Or other relevant type depending on the stream
                })
                player.play();
            });
        });

        onBeforeUnmount(() => {
            if (player) {
                player.dispose();
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
    height: 480px;
}
</style>