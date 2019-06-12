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

4. 下载相关库：
    > cnpm install --save vue-resource  
    > cnpm install element-ui   
    > cnpm install xe-utils vue-element-extends  
    > cnpm install --save xe-ajax  
    > cnpm install --save xe-utils  
    > pip install Flask  
    > pip install flask-cors --upgrade
5. 进入lab3-BankManage\bankManage目录，在命令行中输入下面的命令：
    > cnpm install   
    > cnpm run dev

6. 打开浏览器，在地址栏输入[http://localhost:8080/](http://localhost:8080/)可以对网页进行访问


## 页面路由
+ 将需要路由的页面加入lab3-BankManage\bankManage\src\router\index.js，格式可以仿照已有的条目
+ 在需要进行页面切换时，在脚本中使用下面的方法进行切换
    ```js
    this.$router.push({path:'/register'});
    ```        

## 表格
在网上找到了一个开源可编辑表格[vue-element-extends](https://github.com/xuliangzhan/vue-element-extends)，可以使用它来实现数据的增删改查功能。


## 前后端交互
### 通用
在前端使用下面的代码发送信息给后端，以及解析后端发送的响应报文：

```js
    this.$http.post('http://' + document.domain + ':5000/register', {
        type: this.type,
        username: this.username,
        password: this.password
        //发送给后端的信息，可以按照需求增加条目
    },{  
        emulateJSON:true  //必需，否则可能会json解析出错
    }).then(function (response) {
        //response.body是报文的主体内容
        if (parseInt(response.body.code) === 200){
            ...      
        }                
    })
```

在后端使用下面的代码解析前端发送的信息，并发送响应报文：

```python
    # 解析前端发送的信息
    username=request.form['username']
    password=request.form['password']
    account_type=request.form['type']

    # 给前端发送响应报文
    response = make_response(jsonify({    
                                        'code':200,
                                        'msg':'ok'
                                        # 报文的主体，可以按需求增加条目
                                    })
                                )
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

```

### 增删改查功能的实现
1. 查询:
   + type="Search"
   + 前端会将用户在查询栏中的输入都发送给后端，后端将这些输入组织成SQL语句，从数据库中查询得到结果
   + 后端将查询结果按照既定的格式组织，发送给前端（每一张表的数据格式在Python代码中都有样例，实测确保符合样例格式的数据可以在前端正常显示）
   + 有关字符串的查询都是不精确匹配，只要求用户的输入被该字段包含（子串），输入为空代表对该字段无约束
   + 关于有序量的查询（数值、日期），前端会提供上下界：如果上界为空代表无上界，下界为空代表无下界
2. 删除：
   + type="Delete"
   + 前端会将被删除记录的主键发送给后端
   + 后端组织SQL语句，对数据库进行删除，向前端反馈删除是否成功 
3. 修改：
   + type="Update"
   + 前端会将被修改记录的主键和所有字段的值都发送给后端  
   + 后端组织SQL语句，对数据库进行修改，向前端反馈修改是否成功 
4. 增加：
   + type="Update"
   + 前端会将新增记录所有字段的值都发送给后端，注意被修改记录的主键也会被发送，但是它为null
   + 后端组织SQL语句，对数据库进行增加，向前端反馈增加是否成功

## 身份确认（未实现）
只是一个想法：在登录时，后端给前端提供一个token，token的本质是后端生成的一个随机数（在每一次收到登录请求时随机生成），并将其和用户信息存入一个全局map（Python中的字典）。在登录之后，前端的每一次请求都要附加上这一个token，后端只有在map查到这个token后才能向其发送数据，否则发送错误报文。如果一个token长时间（20分钟）未使用，就将其从map中删除。这样，即使前端可以通过URL跳转到无权访问的页面，它也无法得到数据库中的数据。

## 未解决的问题
+ 客户与员工的联系应当如何处理，在哪一张表格中显示
+ 账户管理
  + 每一个账户可能存在多个户主，应该如何在前端显示（我目前的解决方法是将多个户主的名字使用逗号分隔，作为同一个字段的内容，但是显然不能允许用户随意修改）
  + 根据户主（名字，身份证号）搜索账户需要存储过程的支持，因为这跨越了多张表
  + 更改户主可能需要进一步实现（这是一个外键，最好的做法是提供客户列表供用户选择）
+ 贷款管理
  + 同样的，贷款人也可能有多个
  + 贷款的多次支付应当如何在前端显示
  + 发放贷款需要存储过程支持，由于涉及多个外键，最好也要有列表
+ 业务统计
  + 如何理解题意
  + 如何从后端向前端发送图片。一个tricky的做法，将图片保存到指定位置，前端使用\<img>标记以该位置为src显示图片
  
  
