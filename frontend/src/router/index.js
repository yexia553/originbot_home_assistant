import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'home',
        redirect: '/voice-control',
        component: () => import('../views/Main.vue'),
        children: [
            {
                path: '/voice-control',
                name: 'voice-control',
                component: () => import('../views/home/Home.vue'),
            },
            {
                path: '/monitor',
                name: 'monitor',
                component: () => import('../views/monitor/Monitor.vue'),
            },
        ]
    },
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router