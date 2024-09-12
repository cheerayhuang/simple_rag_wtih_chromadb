import {defineConfig} from 'vite';
import vue from '@vitejs/plugin-vue';

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    server: {
        // 配置代理规则
        proxy: {
            '/api': {
                target: 'http://localhost:8000', // 目标服务器地址
                changeOrigin: true, // 是否改变源地址
                rewrite: (path) => path.replace(/^\/api/, ''), // 重写路径
            },
        },
    },
});