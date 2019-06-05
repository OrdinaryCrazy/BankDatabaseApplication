<template>
    <form validate>
        <h1>注册界面</h1>       
            <label > 账户类型 &nbsp;&nbsp;&nbsp;</label>
            <input type="radio" name="type" value="管理" required=true>管理账户&emsp;
            <input type="radio" name="type" value="支行" required=true>支行账户&emsp;
            <input type="radio" name="type" value="客户" required=true>客户账户&nbsp;
        <br/><br/>
        <label for="username">用&nbsp;&nbsp;户&nbsp;&nbsp;名&emsp;</label>
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
        <label for="password">密&emsp;&emsp;码&emsp;</label>
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

        <label for="password2">重复密码&emsp;</label>
        <input 
            type="password" 
            placeholder="Please enter your password again" 
            id="password2"
            v-model="password2"
            required=true
            style=" width:300px;
                    font-family: 'Fira Code', '汉仪南宫体简';
                    "
        ><br/><br/>
        <button class="button" v-on:click="submit"> <span>提交</span> </button>
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
        submit: function () {           
           //TODO
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
