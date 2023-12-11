<template>
    <div>
        <!-- Other content -->

        <!-- Use VideoPlayer component with :url prop -->
        <VideoPlayer :url="'http://10.11.12.173:8001/hls/test.m3u8'" />

        <!-- Other content -->
    </div>
</template>

<script>
// Import VideoPlayer component
import VideoPlayer from '../../components/VideoPlayer.vue';

export default {
    components: {
        VideoPlayer // Register VideoPlayer component
    },

    // Other options...
};
</script>

<!-- Other styles or scripts as needed -->
