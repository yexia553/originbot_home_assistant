<template>
    <el-main><VoiceControl /></el-main>
</template>

<script>
import VoiceControl from '../voice_control/VoiceControl.vue'
export default {
    components: {
        VoiceControl,
    }
}
</script>

<style lang="less" scoped>
.el-container {
    height: 100%;

    .el-header {
        padding: 0%;
        display: flex;
        justify-content: space-between;
        align-items: left;
        width: 100%;
        flex-direction: column;
        height: 100px;
        background-color: #333;
    }

    .el-footer {
        padding: 0%;
    }
}
</style>