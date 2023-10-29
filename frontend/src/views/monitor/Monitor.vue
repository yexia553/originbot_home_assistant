<template>
    <el-container direction="vertical">
        <el-header>视频监控</el-header>
        <el-main>
            <div class="video-container">
                <video ref="videoPlayer" autoplay></video>
            </div>
        </el-main>
    </el-container>
</template>

<script setup>
import { ref, onMounted } from "vue";

let videoPlayer = ref(null);

onMounted(async () => {
    const streamUrl = 'http://192.168.0.120/api/monitor/video-stream/';

    // Fetching the stream and playing it in our video player.
    const response = await fetch(streamUrl);
    const blob = await response.blob();
    const objectURL = URL.createObjectURL(blob);
    videoPlayer.value.src = objectURL;
});

</script>

<style scoped>
.video-container {
    display: flex;
    justify-content: center;
}
</style>
