<template>
    <form validate>
        <h1>欢迎使用银行管理系统</h1>
        <button class="button" v-on:click="go"> <span>跳转到登录界面</span> </button>
    </form>
</template>

<script>
export default {
    methods: {
        go: function () {
            this.$router.push('/login')
        }
    }
}
</script>

<style>

</style>
