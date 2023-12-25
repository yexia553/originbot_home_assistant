import request from "./request.js";


export default {
    login(params) {
        return request({
            url: '/api/token/',
            method: 'post',
            data: params,
        })
    },
    refreshToken(params) {
        return request({
            url: '/api/token/refresh',
            method: 'post',
            data: params,
        })
    },
    getRTMPToken() {
        return request({
            url: '/api/monitor/rtmp-token',
            method: 'get',
        })
    },
}
