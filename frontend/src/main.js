import './assets/main.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { createApp } from 'vue'
import App from './App.vue'
import store from './store/index.js'
import router from './router/index.js'
import api from './api/api.js'

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

router.beforeEach((to, from, next) => {
    store.commit('getAccessToken')
    const token = store.state.access_token
    if (!token && to.name !== 'login') {
        next({ name: 'login' })
    } else if (token && to.name === 'login') {
        next({ name: 'home' })
    } else (
        next()
    )
})

app.use(router)
app.use(ElementPlus)
app.mount('#app')
app.config.globalProperties.$api = api