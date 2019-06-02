import Vue from 'vue'
import Router from 'vue-router' /* 引入了路由插件vue-router */
import HelloWorld from '@/components/HelloWorld'

// import login from '@/views/login'

Vue.use(Router) /* 显式声明要用路由 Vue.use(Router) */

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    }
  ]
})
