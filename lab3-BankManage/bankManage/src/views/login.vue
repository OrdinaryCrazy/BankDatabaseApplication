/* 登录界面 */
<template>
    <html>
    <form validate @submit.native.prevent>
        <h1>登录界面</h1>
    <!--======================================================================-->
        <label for="custype"> 登录类型 </label>
            <select id = "custype">
                <option value="SUB_BANK"> 管理 </option>
                <option value="EMPLOYEE"> 支行 </option>
                <option value="CUSTOMER"> 员工 </option>
                <option value="CUSTOMER"> 客户 </option>
            </select>
    <!--======================================================================-->
        <label for="username">用户名</label>
        <input 
            type="text" 
            placeholder="Please enter your username" 
            id="username"
            v-model="username"
            required=true
            style=" width:300px;
                    font-family: 'Fira Code', '汉仪南宫体简';
                    "
        ><br/><br/>
    <!--======================================================================-->
        <label for="password">密码</label>
        <input 
            type="password" 
            placeholder="Please enter your password" 
            id="password"
            v-model="password"
            required=true
            style=" width:300px;
                    font-family: 'Fira Code', '汉仪南宫体简';
                    "
        ><br/><br/>
    <!--=================================================================================-->
        <div id=demo></div>
    </form>
    <!--=================================================================================-->
    <button class="button" v-on:click="login">      <span>登录</span> </button>
    <button class="button" v-on:click="register">   <span>注册</span> </button>
    <!--=================================================================================-->
    </html>
</template>

<script>
import { type } from 'os';
export default {
    name: 'login',
    data: function () {
        return {
            username: '',
            password: '',
            custype: '',
        }
    },
    methods: {
        login: function () {
            var _this = this;
            /* 向后台发送用户名和密码 */
            _this.$http.post('http://' + document.domain + ':5000/login', {
                username:   _this.username,
                password:   _this.password,
                custype:    _this.custype
            },{
                emulateJSON:true  
            }).then( function (response) {
                console.log(response.data);
                //================== DEBUG ========================
                // this.$router.push( { path:'/index' } );
                // 在这里跳转是没有问题的
                //================== DEBUG ========================
                if( parseInt(response.data.code) === 400 ) {
                    // 登录失败
                    _this.username = '';
                    _this.password = '';
                    window.alert("登录失败，请检查用户名和密码是否错误");
                    //================== DEBUG ========================
                    // this.$router.push( { path:'/index' } );
                    // 在这里跳转是没有问题的
                    //================== DEBUG ========================
                } else if ( parseInt(response.data.code) === 200 ) {
                    window.alert("登录成功");
                    // 存token
                    sessionStorage.setItem('token', response.data.token);
                    // 登录成功,跳转到index
                    _this.$router.push( { path:'/index' } );
                    // 在这里就不行 会变成 http://localhost:8080/?
                    // BUG原因：form 中的 button 会触发页面自动刷新
                }
                else {
                    window.alert("未知错误");
                }
            }).catch(function (error) {
                console.log(error);
            })
        },
        register: function() {
            this.$router.push({path:'/register'});
        }
    }
}

</script>

<style>
.button {
    display: inline-block;
    border-radius: 4px;
    background-color: #f4511e;
    border: none;
    color: #FFFFFF;
    text-align: center;
    font-size: 12px;
    padding: 20px;
    width: 120px;
    transition: all 0.5s;
    cursor: pointer;
    margin: 5px;
    font-family: 'Fira Code', '汉仪南宫体简';
    font-size:20px;
}

.button span {
    cursor: pointer;
    display: inline-block;
    position: relative;
    transition: 0.5s;
}

.button span:after {
    content: '»';
    position: absolute;
    opacity: 0;
    top: 0;
    right: -20px;
    transition: 0.5s;
}

.button:hover span {
    padding-right: 25px;
}

.button:hover span:after {
    opacity: 1;
    right: 0;
}
</style>
