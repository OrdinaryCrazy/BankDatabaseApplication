/* 入口界面 */
/* 这是一个视图(或者说组件和页面)，相当于一个容器 */
/* 在Vue中，官网叫它做组件，单页面的意思，
 * 是结构，样式，逻辑代码都写在同一个文件中，
 * 当我们引入这个文件后，就相当于引入对应的结构、样式和JS代码 
 */

<template>
    <div id="app">
        <router-view></Login></router-view>
    </div>
</template>

<script>
import Login from '@/views/login.vue'
export default {
    name: 'App',
    components: {
        Login
    }
}
</script>

<style>
#app {
    font-family: 'Fira Code', '汉仪南宫体简', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #1070cf;
    margin-top: 60px;
}
</style>
