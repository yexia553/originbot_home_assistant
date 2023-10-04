<template>
    <div>
        <div>
            <el-row>
                <div class="demo-basic--circle">
                    <el-avatar shape="square" :size="small" :src="getImgSrc()" />
                </div>
                <div class="sub-title">OriginBot Home Assistant</div>
            </el-row>
        </div>
        <div>
            <el-row class="sub-menu">
                <div class="flex">
                    <el-button type="primary">语音控制
                        <el-icon :style="{ marginLeft: '5px' }">
                            <Mic />
                        </el-icon>
                    </el-button>
                </div>
            </el-row>
        </div>
    </div>
</template>

<script>
export default {
    setup() {
        let getImgSrc = () => {
            return new URL("../assets/images/originbot.png", import.meta.url).href;
        };
        return {
            getImgSrc,
        }
    }
}

</script>

<style lang="less" scoped>
.demo-basic--circle {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-left: 30px;
    margin-right: 15px;
    margin-top: 5px;
    margin-bottom: 2px;
}

.sub-title {
    margin-top: 7px;
    margin-left: 10px;
    margin-bottom: 2px;
    font-size: 20px;
    color: #fff;
}

.sub-menu {
    margin-left: 30px;
    margin-top: 10px;
    height: 20px;
}
</style>