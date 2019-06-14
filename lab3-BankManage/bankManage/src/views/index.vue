<template>
    <div>
        <h1>欢迎使用银行管理系统</h1>
        <div v-html="message"></div>
        <br />
        <div>
            <button class="buttonred" v-on:click="goBank" v-if="type == 'SUB_BANK'">
                <span>支行管理</span>
            </button>
            <button class="buttonred" v-on:click="goStaff" v-if="type == 'EMPLOYEE' || type == 'SUB_BANK'">
                <span>员工管理</span>
            </button>
            <button class="buttonred" v-on:click="goCustomer" v-if="type == 'CUSTOMER' || type == 'SUB_BANK'">
                <span>客户管理</span>
            </button>
            <br v-if="type == 'SUB_BANK'" />
            <br v-if="type == 'SUB_BANK'" />
            <button class="buttonred" v-on:click="goAccount" v-if="type == 'EMPLOYEE' || type == 'SUB_BANK' || type == 'CUSTOMER'">
                <span>账户管理</span>
            </button>
            <button class="buttonred" v-on:click="goLoan" v-if="type == 'EMPLOYEE' || type == 'SUB_BANK' || type == 'CUSTOMER'">
                <span>贷款管理</span>
            </button>
            <button class="buttonred" v-on:click="goSummary" v-if="type == 'SUB_BANK'">
                <span>业务统计</span>
            </button>
            <button class="buttonred" v-on:click="exit">
                <span>退出登录</span>
            </button>
        </div>
        <br /><br /><br />
        <div align="right"></div>
    </div>
</template>

<script>
export default {
    name: "Index",
    data() {
        return {
            type: "",
            message: ""
        };
    },
    created() {
        this.type = localStorage.getItem("type");
        if (this.type != "EMPLOYEE" && this.type != "SUB_BANK" && this.type != "CUSTOMER") {
            this.$router.push("/404");
        }
        switch (this.type) {
            case "SUB_BANK":
                this.message = "<h2>账户类型：支行账户</h2><h2>支行名：" + localStorage.getItem("username") + "</h2>";
                break;
            case "EMPLOYEE":
                this.message = "<h2>账户类型：员工账户</h2><h2>身份证号：" + localStorage.getItem("username") + "</h2>";
                break;
            case "CUSTOMER":
                this.message = "<h2>账户类型：客户账户</h2><h2>身份证号：" + localStorage.getItem("username") + "</h2>";
                break;
        }

        console.log(type);
    },
    methods: {
        goSummary: function() {
            this.$router.push("/summary");
        },
        goBank: function() {
            this.$router.push("/bank");
        },
        goStaff: function() {
            this.$router.push("/staff");
        },
        goCustomer: function() {
            this.$router.push("/customer");
        },
        goAccount: function() {
            this.$router.push("/account");
        },
        goLoan: function() {
            this.$router.push("/loan");
        },
        exit: function() {
            localStorage.setItem("type", null);
            this.$router.push("/");
        }
    }
};
</script>

<style>
.buttonred {
    font-family: "Fira Code", "汉仪南宫体简";
    display: inline-block;
    border-radius: 4px;
    background-color: #f4511e;
    border: none;
    color: #ffffff;
    text-align: center;
    font-size: 18px;
    padding: 20px;
    width: 150px;
    transition: all 0.5s;
    cursor: pointer;
    margin: 5px;
}

.buttonred span {
    cursor: pointer;
    display: inline-block;
    position: relative;
    transition: 0.5s;
}
.buttonred:hover span:after {
    opacity: 1;
    right: 0;
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
</style>
