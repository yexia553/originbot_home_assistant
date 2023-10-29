import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'home',
        component: () => import('../views/home/Home.vue'),
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