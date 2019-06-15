<template>
    <html>
        <h1>您要查看的页面不存在或已删除</h1>
        <h2>点击图片返回首页</h2>
        <el-button @click="f()" > 34242</el-button>
        <a href="/"><img src='static/404.jpg'></img></a>
        
    </html>
</template>

<script>
import { MessageBox, Message } from "element-ui";
export default {
    data: function() {
        return {

        };
    },
    methods: {
        f() {
        //const h = this.$createElement;
        this.$message({
          message:  "hello"
        });
      }
    }
};
</script>

<style>

</style>
