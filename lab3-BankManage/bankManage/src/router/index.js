//  import Vue from "vue";
//  import Router from "vue-router"; /* 引入了路由插件vue-router */
import index from '@/views/index.vue'
import register from '@/views/register.vue'
import login from '@/views/login'

const routers = [
  {
    path: '/register',
    name: 'Register',
    component: register
  },
  {
    path: '/',
    name: 'Login',
    component: login
  }
]

export default routers
