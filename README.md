# BankDatabaseApplication
This is a personal USTC 011147 Course work repository aims at designing and implementing a database application.
# Lab3 银行管理系统
## 实验环境
+ win10环境
+ Vuejs前端(3.8.2) 
+ Flask后端(Flask1.0.3 Flask-Cors3.0.7 + Oracle 18.3)
+ 编程语言
  + 前端：html+css+JavaScript
  + 后端：python

## 环境配置
1. 下载npm：
    + 参考网页：https://www.runoob.com/vue2/vue-install.html
    + 先下载NodeJS，可以去[官网](https://nodejs.org/en/download/)下载，在Windows10平台上可以下载64位msi文件进行安装
    + 安装完毕后，可以在命令行中使用下面的命令判断是否安装成功
        > npm -v

2. 使用淘宝npm镜像：
    > npm install -g cnpm --registry=https://registry.npm.taobao.org

3. 下载vue.js：
    > cnpm install vue  
    > cnpm install --global vue-cli

4. 进入lab3-BankManage\bankManage目录，在命令行中输入下面的命令：
    > cnpm install  
    > cnpm install --save vue-resource  
    > cnpm run dev

5. 打开浏览器，在地址栏输入[http://localhost:8080/](http://localhost:8080/)可以对网页进行访问


## 页面路由
+ 将需要路由的页面加入lab3-BankManage\bankManage\src\router\index.js，格式可以仿照已有的条目
+ 在需要进行页面切换时，在脚本中使用下面的方法进行切换
    ```js
    this.$router.push({path:'/register'});
    ```        