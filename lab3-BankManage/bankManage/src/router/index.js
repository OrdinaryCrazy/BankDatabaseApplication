//  import Vue from "vue";
//  import Router from "vue-router"; /* 引入了路由插件vue-router */
import index from '@/views/index.vue'
import register from '@/views/register.vue'
import login from '@/views/login'
import bank from '@/views/bank'
import staff from '@/views/staff'
import customer from '@/views/customer'
import account from '@/views/account'  
import loan from '@/views/loan'
import summary from '@/views/summary'

const routers = [
{
    path: '/register',
    name: 'Register',
    component: register
},
{
    path: '/index',
    name: 'Index',
    component: index
},
{
    path: '/',
    name: 'Login',
    component: login
},
{
  path: '/bank',
  name: 'Bank',
  component: bank
},
{
  path: '/staff',
  name: 'Staff',
  component: staff
},
{
  path: '/customer',
  name: 'Customer',
  component: customer
},
{
  path: '/account',
  name: 'Account',
  component: account
},
{
  path: '/loan',
  name: 'Loan',
  component: loan
},
{
  path: '/summary',
  name: 'Summary',
  component: summary
}
]

export default routers
