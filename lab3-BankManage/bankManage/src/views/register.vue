<template>
    <form validate onSubmit="return false">
        <h1>注册界面</h1>       
            <label > 账户类型 &nbsp;&nbsp;&nbsp;</label>
            <input type="radio" name='type' v-model="type" value="管理" required=true>管理账户&emsp;
            <input type="radio" name='type' v-model="type" value="支行" required=true>支行账户&emsp;
            <input type="radio" name='type' v-model="type" value="客户" required=true>客户账户&nbsp;
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
        <label style='font-family:汉仪南宫体简;color:red;font-size:15px;' >注：用户名和密码必须由字母或数字组成，且密码长度不能小于6。</label>
        <br>
       
        <button class="button" v-on:click="submit()"> <span>提交</span> </button>
        <div id=demo></div>
    </form>
</template>

<script>
export default {
    name: 'login',
    data: function () {
        return {
            type: '',
            username: '',
            password: '',
            password2: ''
        }
    },
    methods: {
        submit: function () {      
            //console.log(this.type);    
            if (this.type=="" || this.username==""){
                return;
            }      
            for (var i=0;i<this.username.length;i++){
                var x=this.username.charAt(i);
                if (!((x>='0'&&x<='9')||(x>='a'&&x<='z')||(x>='A'&&x<='Z'))){
                    window.alert("用户名非法");
                    return;
                }
            }
            for (var i=0;i<this.password.length;i++){
                var x=this.password.charAt(i);
                if (!((x>='0'&&x<='9')||(x>='a'&&x<='z')||(x>='A'&&x<='Z'))){
                    window.alert("密码非法");
                    return;
                }
            }
            if (this.password.length<6){
                window.alert("密码过短");
                return;
            }
            if (this.password!==this.password2){
                window.alert("两次输入的密码不相同");
            }   
            else {
                this.$http.post('http://' + document.domain + ':5000/register', {
                    type: this.type,
                    username: this.username,
                    password: this.password
                },{  
                    emulateJSON:true  
                }).then(function (response) {
                    //console.log(response.status);
                    if (parseInt(response.body.code) === 200){
                        
                        //console.log("OK");
                        this.$router.push('/index');
                        window.alert("注册成功");
                        //return;                       
                    }
                    else if (parseInt(response.body.code) === 400) {
                        window.alert("用户名已存在");
                    }
                    else {
                        window.alert("注册失败");
                    }                   
                }                
                )
            }                
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
