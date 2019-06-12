<template>
    <div>
        <h1>欢迎使用银行管理系统</h1>
        <button class="buttonred" v-on:click="goBank">      <span>支行管理</span> </button>
        <button class="buttonred" v-on:click="goStaff">     <span>员工管理</span> </button>
        <button class="buttonred" v-on:click="goCustomer">  <span>客户管理</span> </button>
        <button class="buttonred" v-on:click="goAccount">   <span>账户管理</span> </button>
        <button class="buttonred" v-on:click="goLoan">      <span>贷款管理</span> </button>
        <button class="buttonred" v-on:click="goSummary">   <span>业务统计</span> </button>
        <br><br><br>
    </div>
</template>

<script>
export default {
    name:'Index',
    data () {
        return {

        }
    },
    methods: {
        goSummary: function () {      
            this.$router.push('/summary');
        },
        goBank: function() {
            this.$router.push('/bank');
        },
        goStaff: function(){
            this.$router.push('/staff');
        },
        goCustomer: function(){
            this.$router.push('/customer');
        },
        goAccount: function(){
            this.$router.push('/account');
        },
        goLoan: function(){
            this.$router.push('/loan');
        }
    }
}
</script>

<style>
.buttonred {
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
</style>
