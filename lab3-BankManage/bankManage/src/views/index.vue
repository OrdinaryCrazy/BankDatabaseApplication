<template>
    <div>
        <h1>欢迎使用银行管理系统</h1>
        <button class="button" v-on:click="goBank"> <span>支行管理</span> </button>
        <button class="button" v-on:click="go"> <span>员工管理</span> </button>
        <button class="button" v-on:click="go"> <span>客户管理</span> </button>
        <button class="button" v-on:click="go"> <span>账户管理</span> </button>
        <button class="button" v-on:click="go"> <span>贷款管理</span> </button>
        <button class="button" v-on:click="go"> <span>业务统计</span> </button>
        <br><br><br>
    </div>
</template>

<script>
export default {
    methods: {
        go: function () {      
                  
        },
        goBank: function() {
          this.$router.push('/bank');
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
.button:hover span:after {
  opacity: 1;
  right: 0;
}
</style>
