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
    background-repeat: repeat-y;
    background-attachment: scroll;
}
.body {
    display: flex;
    flex-flow: column;
    min-height: 70vh;
}
body .el-table th.gutter {
    display: table-cell !important;
}
body .table {
    border: 2px solid #429fff; /* 表格边框 */
    font-family: "汉仪南宫体简";
    font-size: 18px;
    border-collapse: collapse; /*边框重叠 */
    overflow-x: auto;
    overflow-y: auto;
}
body .table tr:hover {
    background-color: #d2e8ff; /* 动态变色,IE6下无效！*/
}
body .table caption {
    padding-top: 3px;
    padding-bottom: 2px;
    font: bold 1.1em;
    color: #ff00ff;
    background-color: #f0f7ff;
    border: 1px solid #429fff; /* 表格标题边框 */
}
body .table th {
    border: 1px solid #429fff; /* 行、列名称边框 */
    background-color: #d2e8ff;
    font-weight: bold;
    padding-top: 4px;
    padding-bottom: 4px;
    padding-left: 10px;
    padding-right: 10px;
    text-align: center;
}
body .table tr {
    background-color: rgb(240,240,240);
}
body .table td {
    border: 1px solid #429fff; /* 单元格边框 */
    text-align: center;
    padding: 4px;
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
