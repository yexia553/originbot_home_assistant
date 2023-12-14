<template>
    <div>
        <!-- Other content -->

        <!-- Use VideoPlayer component with :url prop -->
        <VideoPlayer :url="'ws://10.11.12.173:8000/ws/babycare/'" />

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
