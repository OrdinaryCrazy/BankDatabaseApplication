<template>
    <form validate>
        <h1>登录界面</h1>
        <label for="custype"> 登录类型 </label>
            <select id = "custype">
                <option value="SUB_BANK"> 管理 </option>
                <option value="EMPLOYEE"> 支行 </option>
                <option value="CUSTOMER"> 客户 </option>
            </select>
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
        <label for="password">密码</label>
        <input 
            type="text" 
            placeholder="Please enter your password" 
            id="password"
            v-model="password"
            required=true
            style=" width:300px;
                    font-family: 'Fira Code', '汉仪南宫体简';
                    "
        ><br/><br/>
        <button class="button" v-on:click="login"> <span>登录</span> </button>
        <button class="button" v-on:click="login"> <span>注册</span> </button>
        <div id=demo></div>
    </form>
</template>

<script>
export default {
    name: 'login',
    data: function () {
        return {
            username: '',
            password: ''
        }
    },
    methods: {
        login: function () {
            // window.alert(this.username)
            this.$http.post('http://' + document.domain + ':5000/login', {
                username: this.username,
                password: this.password
            }).then(function (response) {
                console.log(response.data);
                if(parseInt(response.data.code) === 400){
                // 登录失败
                this.username = '';
                this.password = '';
                window.alert("登录失败，请检查用户名和密码是否错误")
                } else if (parseInt(response.data.code) === 200){
                    // 存token
                    sessionStorage.setItem('token', response.data.token);
                    // 登录成功,跳转到index
                    // this.$router.push('index')
                    window.alert("登录成功")
                    // document.getElementById('demo').innerHTML = "登录成功"
                }
            })
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
  width: 100px;
  transition: all 0.5s;
  cursor: pointer;
  margin: 5px;
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
