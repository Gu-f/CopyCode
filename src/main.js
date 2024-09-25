import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';
import CodeInfo from './components/CodeInfo.vue';
import Home from './components/Home.vue';  // 引入新的 Home.vue

const routes = [
  {
    path: '/',  // 根路径
    name: 'Home',
    component: Home,  // 渲染 Home 组件
  },
  {
    path: '/code/:codeId',  // 定义带有变量参数的路由
    name: 'Codeinfo',
    component: CodeInfo,
    props: true  // 将路由参数作为 props 传递给组件
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

createApp(App)
  .use(router)
  .mount('#app');
