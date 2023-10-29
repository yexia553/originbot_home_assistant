<template>
    <div class="common-layout">
        <el-container>
            <el-header>
                <CommonHeader />
            </el-header>
            <el-main><router-view></router-view></el-main>
            <el-footer>
                <CommonFooter />
            </el-footer>
        </el-container>
    </div>
</template>

<script>
import CommonHeader from '../../components/CommonHeader.vue'
import CommonFooter from '../../components/CommonFooter.vue'
// import VoiceControl from '../voice_control/VoiceControl.vue'
export default {
    components: {
        CommonHeader,
        CommonFooter,
        // VoiceControl,
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