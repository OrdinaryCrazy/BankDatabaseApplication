/* 入口界面 */ /* 这是一个视图(或者说组件和页面)，相当于一个容器 */ /* 在Vue中，官网叫它做组件，单页面的意思， * 是结构，样式，逻辑代码都写在同一个文件中， *
当我们引入这个文件后，就相当于引入对应的结构、样式和JS代码 */

<template>
    <div id="app">
        <div class="body">
            <router-view></router-view>
        </div>
        <br />
        <br />
        <br />
        <footer class="footer">
            <hr />
            <p>
                中国科学技术大学 计算机科学与技术学院<br />
                2019年春季学期 数据库系统及应用课程实验<br />
                &copy;张劲暾 王浩宇 吴雨菲
            </p>
        </footer>
    </div>
</template>

<script>
import Login from "@/views/login.vue";
import Index from "@/views/index.vue";
export default {
    name: "App",
    components: {
        Login,
        Index
    }
};
</script>

<style>
#app {
    font-family: "Fira Code", "汉仪南宫体简", Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #1070cf;
    margin-top: 60px;
    min-height: 600px;
}
html {
    height: 100%;
    margin: 0;
    padding: 0;
    background-image: url("../static/background3.jpg");
    background-size: cover;
    background-position: center center;
    background-repeat: repeat-x;
    background-attachment: scroll;
}
.body {
    display: flex;
    flex-flow: column;
    min-height: 70vh;
}

.footer {
    font-family: "Fira Code", "汉仪南宫体简";
    font-size: 14px;
    color: grey;
    text-align: center;
    height: 40px;
    width: 100%; /*展开footer宽度*/
}
</style>
