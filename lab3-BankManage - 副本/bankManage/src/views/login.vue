/* 登录界面 */
<template>
    <html>
        <form validate @submit.native.prevent class="form">
            <h1>登录界面</h1>
            <!--======================================================================-->
            <label for="custype"> 登录类型 </label>
            <select id="custype" v-model="custype" class="dropbtn">
                <option value="SUB_BANK"> 支行账户 </option>
                <option value="EMPLOYEE"> 员工账户 </option>
                <!-- <option value="CUSTOMER"> 员工 </option> -->
                <option value="CUSTOMER"> 客户账户 </option>
            </select>
            <!--======================================================================-->
            <label v-if="custype == 'SUB_BANK'">支行名称</label>
            <label v-else>身份证号</label>
            <input
                class="input"
                type="text"
                placeholder="Please enter your username"
                id="username"
                v-model="username"
                required="true"
                style=" width:300px;
                    font-family: 'Fira Code', '汉仪南宫体简';
                    "
            /><br /><br />
            <!--======================================================================-->
            <label for="password">密码</label>
            <input
                class="input"
                type="password"
                placeholder="Please enter your password"
                id="password"
                v-model="password"
                required="true"
                style=" width:300px;
                    font-family: 'Fira Code', '汉仪南宫体简';
                    "
            /><br /><br />
            <!--=================================================================================-->
            <div id="demo"></div>
        </form>
        <!--=================================================================================-->
        <button class="buttonred" v-on:click="login"><span>登录</span></button>
        <button class="buttonred" v-on:click="register"><span>注册</span></button>
        <!--=================================================================================-->
    </html>
</template>

<script>
import { type } from "os";
export default {
    name: "login",
    data: function() {
        return {
            username: "",
            password: "",
            custype: ""
        };
    },
    created() {
        var permission = localStorage.getItem("type");
        if (permission == "SUB_BANK" || permission == "EMPLOYEE" || permission == "CUSTOMER") {
            this.$router.push("/index");
        }
        this.custype = "SUB_BANK";
    },
    methods: {
        login: function() {
            if (this.username == "" || this.password == "") {
                window.alert("用户名和密码不能为空");
                return;
            }
            var _this = this;
            /* 向后台发送用户名和密码 */
            _this.$http
                .post(
                    "http://" + document.domain + ":5000/login",
                    {
                        username: _this.username,
                        password: _this.password,
                        custype: _this.custype
                    },
                    {
                        emulateJSON: true
                    }
                )
                .then(function(response) {
                    console.log(response.data);
                    //================== DEBUG ========================
                    // this.$router.push( { path:'/index' } );
                    // 在这里跳转是没有问题的
                    //================== DEBUG ========================
                    if (parseInt(response.data.code) === 400) {
                        // 登录失败
                        _this.username = "";
                        _this.password = "";
                        window.alert("登录失败，请检查用户名和密码是否错误");
                        //================== DEBUG ========================
                        // this.$router.push( { path:'/index' } );
                        // 在这里跳转是没有问题的
                        //================== DEBUG ========================
                    } else if (parseInt(response.data.code) === 200) {
                        window.alert("登录成功");
                        // 存token
                        localStorage.setItem("type", _this.custype);
                        localStorage.setItem("username", _this.username);
                        //sessionStorage.setItem();
                        // 登录成功,跳转到index
                        _this.$router.push({ path: "/index" });
                        // 在这里就不行 会变成 http://localhost:8080/?
                        // BUG原因：form 中的 button 会触发页面自动刷新
                    } else {
                        window.alert("未知错误");
                    }
                })
                .catch(function(error) {
                    console.log(error);
                });
        },
        register: function() {
            this.$router.push({ path: "/register" });
        }
    }
};
</script>

<style>
.buttonred {
    display: inline-block;
    border-radius: 4px;
    background-color: #f4511e;
    border: none;
    color: #ffffff;
    text-align: center;
    font-size: 12px;
    padding: 20px;
    width: 220px;
    transition: all 0.5s;
    cursor: pointer;
    margin: 5px;
    font-family: "Fira Code", "汉仪南宫体简";
    font-size: 20px;
    box-shadow:0px 1px 2px 1px #aaaaaa,
                inset 0px 1px 1px rgba(255,255,255,0.7);
}

.buttonred span {
    cursor: pointer;
    display: inline-block;
    position: relative;
    transition: 0.5s;
}

.buttonred span:after {
    content: "»";
    position: absolute;
    opacity: 0;
    top: 0;
    right: -20px;
    transition: 0.5s;
}

.buttonred:hover span {
    padding-right: 25px;
}

.buttonred:hover span:after {
    opacity: 1;
    right: 0;
}
.dropbtn {
    border-radius: 6px;
    background-color: rgb(223, 71, 71);
    color: white;
    padding: 4px;
    font-size: 14px;
    border: none;
    cursor: pointer;
    width: 100px;
    height: 40px;
    font-family: "Fira Code", "汉仪南宫体简";
}

.dropdown {
    position: relative;
    border-radius: 4px;
    display: inline-block;
}

.dropdown-content {
    border-radius: 4px;
    display: none;
    position: absolute;
    background-color: #f9f9f9;
    min-width: 160px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
}

.dropdown-content option {
    color: black;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
}

.dropdown-content option :hover {background-color: #f1f1f1}

.dropdown:hover .dropdown-content {
    display: block;
}

.dropdown:hover .dropbtn {
    background-color: #b6f699;
}
.form{
        background: #e0de83;
        width: 760px;
        height: 260px;
        margin: 35px auto;
        padding: 30px;
        box-shadow:0px 2px 4px 2px #aaaaaa,
                   inset 0px 2px 2px rgba(255,255,255,0.7);
        border-radius: 5px;
    }
.input{
    outline-style: none ;
    border: 1px solid #ccc; 
    border-radius: 6px;
    padding: 8px 14px;
    width: 620px;
    font-size: 14px;
    font-weight: 700;
    font-family: "Fira Code", "汉仪南宫体简";
}
.input:focus{
    border-color: #66afe9;
    outline: 0;
    -webkit-box-shadow: inset 0 3px 3px rgba(0,0,0,.075),0 0 8px rgba(102,175,233,.6);
    box-shadow: inset 0 3px 3px rgba(0,0,0,.075),0 0 8px rgba(102,175,233,.6)
}
</style>
