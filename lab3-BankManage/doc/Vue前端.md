### 3.2 VUE前端
Vue前端为用户提供了一个友好的接口，用户在前端的操作会被发送到后端，后端的返回也会被显示在前端。本质上，前端做的只是数据的传递与转换，并不对数据进行处理。
#### 3.2.1 全局路由
##### 3.2.1.1 设计思路
在Vue中，如果要实现页面跳转，必须先将组件注册在路由表中，为其配置路径。之后，就可以通过URL进行跳转。为了实现对用户输入错误URL的处理，错误处理界面的URL被注册为*，即输入任何未注册的URL都会跳转到该界面。
##### 3.2.1.2 路由表
|     页面     |  组件名  |    URL    |
| :----------: | :------: | :-------: |
|   登录界面   |  login   |     /     |
|   注册界面   | register | /register |
|     主页     |  index   |  /index   |
| 支行管理界面 |   bank   |   /bank   |
| 员工管理界面 |  staff   |  /staff   |
| 客户管理界面 | customer | /customer |
| 账户管理界面 | account  | /account  |
| 贷款管理界面 |   loan   |   /loan   |
| 业务统计界面 | summary  | /summary  |
| 错误处理界面 |  error   |     *     |

#### 3.2.2 权限管理
在银行管理系统中，我们设置了三种账户类型：支行账户、员工账户、客户账户，分别对应于三种权限：支行的管理人员、普通员工和普通客户。

##### 3.2.2.1 权限信息的存取
当用户成功登录时，我们将会在本地保存用户的账户类型和用户名（对于支行而言是支行名称，对员工和客户而言是身份证号）。使用下面的JS语句可以进行保存：
```js
localStorage.setItem("type", this.type);
localStorage.setItem("username", this.username);
```
我们也可以通过下面的语句得到保存在本地的权限信息：
```js
this.type = localStorage.getItem("type");
this.username = localStorage.getItem("username");
```
当我们点击“退出登录”按钮时，可以使用下面的语句清空权限信息：
```js
localStorage.setItem("type", null);
localStorage.setItem("username", null);
```

##### 3.2.2.2 粗粒度的权限控制
在前端，可以通过允许或禁止用户访问某些页面实现粗粒度的权限控制。下面是我们的权限表，描述了各个内部界面与三种权限的访问控制关系：

| 权限  | 主页  | 支行管理 | 员工管理 | 客户管理 | 账户管理 | 贷款管理 | 业务统计 |
| :---: | :---: | :------: | :------: | :------: | :------: | :------: | :------: |
| 支行  |   Y   |    Y     |    Y     |    Y     |    Y     |    Y     |    Y     |
| 员工  |   Y   |    N     |    Y     |    N     |    Y     |    Y     |    N     |
| 客户  |   Y   |    N     |    N     |    Y     |    Y     |    Y     |    N     |

这种粗粒度的权限控制是靠下面两种方法实现的：

+ Vue中的v-if属性，该属性可以对组件的显示与否进行条件控制。只有当v-if后面的条件成立时，该组件才会被显示在网页中。例如，下面的代码表明，只有当拥有支行权限时，该按钮才会被显示。通过这样的方法隐藏页面入口，可以阻止用户进入无权访问的页面。
    ```html
    <button v-on:click="goBank" v-if="type == 'SUB_BANK'">
        <span>支行管理</span>
    </button>
    ```
+ Vue中的created()方法，该方法会在页面被创建时调用。我们可以在该页面中对权限进行判断，当权限不足时，自动跳转到错误处理界面。这样，即使用户通过URL进行访问，绕过了上面的权限控制，也无法对页面进行访问。例如，下面的代码是支行管理界面的created()方法。
    ```js
    created() {
        this.permission = localStorage.getItem("type");
        if (this.permission != "SUB_BANK") {
            this.$router.push("/404");
        }
    }
    ```
##### 3.2.2.3 对细粒度的权限控制的探索
上面方法实现的权限控制粒度太粗，当用户进入某个页面时，就默认其拥有了对页面对应的表进行增删改查的所有权限。在实际情况下，我们需要对增删改查进行分别考虑，甚至对于不同的记录，也要进行不同的权限管理。

例如，对于员工账户的员工管理界面，我们实现了更加细粒度的权限控制。

+ 员工信息表
  + 增：不允许
  + 删：不允许
  + 改：只允许修改自己的信息
  + 查：允许
+ 客户联系表
  + 增：只允许增加与自己联系的客户
  + 删：只允许删除与自己联系的客户
  + 改：只允许修改与自己联系的客户
  + 查：允许

这种控制主要通过两种方法实现：一是上面提到的v-if属性，我们使用该属性隐藏员工信息表的“新增”和“删除”按钮；二是通过在按钮绑定的事件中增加权限判定代码，如下面是两个表的“修改”按钮绑定事件的权限判定代码，当修改他人信息时，会弹出警告信息：
```js
openActiveRowEvent(name, row) {
    switch (name) {
        case "elxEditable1":
            if (this.permission != "SUB_BANK" && 
                row.id != localStorage.getItem("username")) {
                Message({ message: "您没有操作权限", type: "warning" });
                return;
            }
            break;
        case "elxEditable2":
            if (this.permission != "SUB_BANK" && 
                row.staffid != localStorage.getItem("username")) {
                Message({ message: "您没有操作权限", type: "warning" });
                return;
            }
            break;
    }
    ...
}
```

由于时间的限制，我们仅仅对这一个界面实现了细粒度的权限管理。但依照类似的方法，可以实现所有界面的细粒度权限管理。

#### 3.2.3 模块概述

##### 3.2.3.1 前后端交互
前端使用POST报文与后端进行交互，并接收后端的响应报文，加以解析，得到后端返回的数据。

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
    ...
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

##### 3.2.3.2 增删改查功能的实现
一般而言，我们使用如下的方法实现增删改查功能。


1. 查询:
   + type="Search"
   + 前端会将用户在查询栏中的输入都发送给后端，后端将这些输入组织成SQL语句，从数据库中查询得到结果
   + 后端将查询结果按照既定的格式组织，发送给前端。后端的查询结果是一个列表，列表的每一个元素都是一个字典（对应表格的一行），字典中将列名与对应的值以键值对的形式存储 
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


#### 3.2.4 登录模块

##### 3.2.4.1 设计思路
该模块的设计比较简单，主要需要用户提供三个输入。一个下拉框用于选择账户类型，一个文本框用于输入用户名，一个密码框用于输入密码。前端将这些数据都发送给后端，后端验证用户名和密码是否正确并予以反馈。

##### 3.2.4.2 向后端发送的数据
+ 目的地址：/login
+ type: 账户类型
+ username: 用户名
+ password: 密码

##### 3.2.4.3 后端反馈的数据
登录是否成功

#### 3.2.5 注册模块

##### 3.2.5.1 设计思路
三种账户类型对应于三张表，因此注册时需要填写的就是表的各个字段名。使用v-if属性，可以在用户选择不同的类型时，向用户提供不同的输入框以填写不同的字段。同时，只有用户名和密码是必填的，其它字段可以为空，此时后端会用默认值填充该字段。

##### 3.2.5.2 向后端发送的数据
+ 目的地址： /register
+ 支行账户
  + type='SUB_BANK'
  + username: 支行名（必填）
  + password: 密码（必填）
  + city: 所在城市
  + money: 资产总额
+ 客户账户
  + type='CUSTOMER'
  + username: 身份证号（必填）
  + password: 密码（必填）
  + name: 姓名
  + tel: 联系电话
  + addr: 家庭住址
  + name_link: 联系人姓名
  + tel_link: 联系人手机号
  + email_link: 联系人Email
  + relation: 联系人与客户关系
+ 员工账户
  + type='EMPLOYEE'
  + username: 身份证号（必填）
  + password: 密码（必填）
  + name: 姓名
  + dept: 所在部门
  + bankname: 所在支行
  + tel: 电话号码
  + addr: 家庭住址
  + date_s: 入职时间

##### 3.2.5.3 后端反馈的数据
注册是否成功


#### 3.2.6 主页模块
这是用户登录后看到的第一个界面，界面上显示了所有可达的子界面，点击对应的按钮即可跳转。同时，该界面显示了用户的账户类型和用户名，并使用v-if属性隐藏了无权访问的界面。此外，点击“退出登录”按钮可以退出登录，回到登录界面。

该界面不与后端进行任何交互。


#### 3.2.7 支行管理模块

##### 3.2.7.1 设计思路
该界面比较简单，只存在一张表格，显示支行的所有信息（对应于数据库中的SUB_BANK表）。该表格提供增、删、改功能。页面另有查询部分，可以对表格进行查询。

##### 3.2.7.2 向后端发送的数据
+ 查询表格内容
  + 目的地址：/bank
  + type: "Search"
  + bankSearch: 支行名称（模糊查询）
  + citySearch: 所在城市（模糊查询）
  + lowerBound: 资产总额下界
  + upperBound: 资产总额上界
+ 删除表格记录
  + 目的地址：/bank
  + type: "Delete"
  + primary: 支行名称（主键）
+ 新增或修改表格记录
  + 目的地址：/bank
  + type: "Update"
  + name: 支行名称
  + city: 所在城市
  + money: 资产总额
  + old_primary: 修改前的支行名称（当新增时为null）

##### 3.2.7.3 后端反馈的数据
+ 查询表格内容：查询得到的结果
+ 新增表格记录：操作成功/错误码+错误原因
+ 修改表格记录：操作成功/错误码+错误原因
+ 删除表格记录：操作成功/错误码+错误原因

#### 3.2.8 客户管理模块

##### 3.2.8.1 设计思路
由于一个客户可能存在多个与之联系的员工，该页面设计为两个表格：主表显示客户所有的信息（对应于数据库中的CUSTOMER表），点击主表中“详情”按钮，可以在子表中显示与之联系的所有员工信息（对应于EMPLOYEE_CUSTOMER表）。每张表格都提供了增、删、改功能。页面另有查询部分，可以对主表进行查询。
##### 3.2.8.2 向后端发送的数据
+ 查询主表内容
  + 目的地址：/customer
  + type: "Search"
  + nameSearch: 姓名（模糊查询）
  + idSearch: 身份证号（模糊查询）
  + telSearch: 电话号码（模糊查询）
  + addrSearch: 家庭住址（模糊查询）
  + linknameSearch: 联系人姓名（模糊查询）
  + linktelSearch: 联系人电话（模糊查询）
  + emailSearch: 联系人Email（模糊查询）
+ 删除主表记录
  + 目的地址：/customer
  + type: "Delete"
  + primary: 身份证号（主键）
+ 新增或修改主表记录
  + 目的地址：/customer
  + type: "Update"
  + id: 身份证号
  + name: 姓名
  + tel: 电话号码
  + addr: 家庭住址
  + name_link: 联系人姓名
  + tel_link: 联系人电话
  + email_link: 联系人Email
  + relation: 联系人与客户关系
  + old_primary: 修改前的身份证号（当新增时为null）
+ 查询子表内容
  + 目的地址：/staffCustomer
  + type: "SearchByCustomer"
  + custid: 客户身份证号
+ 新增或修改子表记录
  + 目的地址：/staffCustomer
  + type: "Update"
  + custID: 客户身份证号
  + staffID: 员工身份证号
  + serviceType: 服务类型
  + old_custID: 修改前的客户身份证号
  + old_staffID: 修改前的员工身份证号（当新增时为null）
+ 删除子表记录
  + 目的地址：/staffCustomer
  + type: "Delete"
  + custID: 客户身份证号（主键）
  + staffID: 员工身份证号（主键）
##### 3.2.8.3 后端反馈的数据
+ 查询主表内容：查询得到的结果
+ 新增主表记录：操作成功/错误码+错误原因
+ 修改主表记录：操作成功/错误码+错误原因
+ 删除主表记录：操作成功/错误码+错误原因
+ 查询子表内容：查询得到的结果
+ 新增子表内容：操作成功/错误码+错误原因  
+ 修改子表记录：操作成功/错误码+错误原因
+ 删除子表内容：操作成功/错误码+错误原因

#### 3.2.9 员工管理模块

##### 3.2.9.1 设计思路
由于一个员工可能存在多个与之联系的客户，该页面设计为两个表格：主表显示员工所有的信息（对应于数据库中的EMPLOYEE表），点击主表中“详情”按钮，可以在子表中显示与之联系的所有客户信息（对应于EMPLOYEE_CUSTOMER表）。每张表格都提供了增、删、改功能。页面另有查询部分，可以对主表进行查询。
##### 3.2.9.2 向后端发送的数据
+ 查询主表内容
  + 目的地址：/staff
  + type: "Search"
  + nameSearch: 姓名（模糊查询）
  + idSearch: 身份证号（模糊查询）
  + bankSearch: 所属支行（模糊查询）
  + telSearch: 电话号码（模糊查询）
  + deptSearch: 所属部门（模糊查询）
  + addrSearch: 家庭住址（模糊查询）
  + lowerBound: 入职日期下界
  + upperBound: 入职日期上界
+ 删除主表记录
  + 目的地址：/staff
  + type: "Delete"
  + primary: 身份证号（主键）
+ 新增或修改主表记录
  + 目的地址：/staff
  + type: "Update"
  + id: 身份证号
  + name: 姓名
  + bank: 所属支行
  + dept: 所属部门
  + tel: 电话号码
  + addr: 家庭住址
  + date_s: 入职日期
  + old_primary: 修改前的身份证号（当新增时为null）
+ 查询子表内容
  + 目的地址：/staffCustomer
  + type: "SearchByStaff"
  + custid: 员工身份证号
+ 新增或修改子表记录
  + 目的地址：/staffCustomer
  + type: "Update"
  + custID: 客户身份证号
  + staffID: 员工身份证号
  + serviceType: 服务类型
  + old_custID: 修改前的客户身份证号（当新增时为null）
  + old_staffID: 修改前的员工身份证号
+ 删除子表记录
  + 目的地址：/staffCustomer
  + type: "Delete"
  + custID: 客户身份证号（主键）
  + staffID: 员工身份证号（主键）
##### 3.2.9.3 后端反馈的数据
+ 查询主表内容：查询得到的结果
+ 新增主表记录：操作成功/错误码+错误原因
+ 修改主表记录：操作成功/错误码+错误原因
+ 删除主表记录：操作成功/错误码+错误原因
+ 查询子表内容：查询得到的结果
+ 新增子表内容：操作成功/错误码+错误原因  
+ 修改子表记录：操作成功/错误码+错误原因
+ 删除子表内容：操作成功/错误码+错误原因

#### 3.2.10 账户管理模块

##### 3.2.10.1 设计思路
由于账户可能存在多个户主，该页面设计为两个表格：主表显示账户所有的信息（对应于数据库中的CHECK_ACCOUNT表和DEPOSIT_ACCOUNT表），点击主表中“显示户主”按钮，可以在子表中显示所有的户主信息（对应于CUSTOMER_CHECK_ACCOUNT表和CUSTOMER_DEPOSIT_ACCOUNT表）。每张表格都提供了增、删、改功能。页面另有查询部分，可以对主表进行查询。
##### 3.2.10.2 向后端发送的数据
+ 查询主表内容
  + 目的地址：/account
  + type: "Search"
  + bankSearch: 支行名称（模糊查询）
  + idSearch: 账户号（模糊查询）
  + ownerSearch: 户主姓名（模糊查询）
  + tpeSearch: 账户类型
  + money_lo: 余额下界
  + money_up: 余额上界
  + open_lo: 开户日期下界
  + open_up: 开户日期上界
+ 删除主表记录
  + 目的地址：/account
  + type: "Delete"
  + primary: 账户号（主键）
  + acctype: 账户类型
+ 新增或修改主表记录
  + 目的地址：/account
  + type: "Update"
  + id: 账户号
  + bank: 支行名称
  + money: 余额
  + ownerid: 开户者ID（只在新增时使用）
  + open_date: 开户日期
  + acctype: 账户类型
  + interest: 利率
  + cashtype: 货币类型
  + overdraft: 透支额
  + old_primary: 修改前的账户号（当新增时为null）
+ 查询子表内容
  + 目的地址：/accountCustomer
  + type: "Search"
  + accid: 账户号
  + bank: 开户支行
  + acctype: 账户类型
+ 新增子表记录
  + 目的地址：/accountCustomer
  + type: "Insert"
  + accid: 账户号
  + bank: 开户支行
  + visit_date: 最近访问日期  
  + ownerid: 户主ID
  + acctype: 账户类型
+ 删除子表记录
  + 目的地址：/accountCustomer
  + type: "Delete"
  + accid: 账户号
  + bank: 开户支行
  + ownerid: 户主ID
  + acctype: 账户类型
##### 3.2.10.3 后端反馈的数据
+ 查询主表内容：查询得到的结果
+ 新增主表记录：操作成功/错误码+错误原因
+ 修改主表记录：操作成功/错误码+错误原因
+ 删除主表记录：操作成功/错误码+错误原因
+ 查询子表内容：查询得到的结果
+ 新增子表内容：操作成功/错误码+错误原因  
+ 删除子表内容：操作成功/错误码+错误原因

#### 3.2.11 贷款管理模块

##### 3.2.11.1 设计思路
由于一笔贷款可能存在多笔支付，该页面设计为两个表格：主表显示贷款所有的信息（对应于数据库中的LOAN表），点击主表中“详情”按钮，可以在子表中显示所有的支付信息（对应于PAY表）。主表提供了增、删功能，子表只提供删除功能。页面另有查询部分，可以对主表进行查询。

##### 3.2.11.2 向后端发送的数据
+ 查询主表内容
  + 目的地址：/loan
  + type: "Search"
  + bankSearch: 放款支行（模糊查询）
  + idSearch: 贷款号（模糊查询）
  + statusSearch: 贷款状态
  + custSearch: 贷款人姓名（模糊查询）
  + upperBound: 贷款金额上界
  + lowerBound: 贷款金额下界
+ 删除主表记录
  + 目的地址：/loan
  + type: "Delete"
  + primary: 贷款号（主键）
+ 新增主表记录
  + 目的地址：/loan
  + type: "Update"
  + loanid: 贷款号
  + bank: 放款支行名称
  + customer: 贷款人身份证号
  + amount: 贷款金额
  + status: '0'
  + old_primary: null
+ 查询子表内容
  + 目的地址：/pay
  + type: "Search"
  + loanid: 贷款号
+ 新增子表记录
  + 目的地址：/pay
  + type: "Insert"
  + loanid: 贷款号
  + date: 支付日期
  + money: 支付金额

##### 3.2.11.3 后端反馈的数据
+ 查询主表内容：查询得到的结果
+ 新增主表记录：操作成功/错误码+错误原因
+ 删除主表记录：操作成功/错误码+错误原因
+ 查询子表内容：查询得到的结果
+ 新增子表内容：操作成功/错误码+错误原因  

#### 3.2.12 业务统计模块

##### 3.2.12.1 设计思想
用户输入统计范围与统计指标，前端将其发给后端。后端据此访问数据库，将统计结果表发给前端。前端根据该表以及用户选择的图像类别，使用开源图表组件v-charts在前端绘制统计图。

##### 3.2.12.2 发送给后端的数据
+ 目的地址： /summary
+ upperBound: 统计时间范围的上界
+ lowerBound: 统计时间范围的下界
+ timegrain: 统计的时间粒度
+ sumtype: 统计的业务
+ datatype: 统计的指标
+ graphtype: "curve"

##### 3.2.12.3 后端反馈的数据
+ columnList: 一个列表，包含所有的支行名称，每一个元素都是一个支行名称的字符串
+ rawData: 一个列表，每一个元素都是一个字典，其中一个键值对的键是'time'，值是该字典对应的统计时间段，其他所有键值对的键都是支行名称，值是支行对应的统计值



##### 3.2.12.4 v-charts的使用
下面的代码用于绘制饼图和折线图，chartData和chartData2用于提供数据源：
```html
<ve-pie :data="chartData" v-if="graphtype=='pie'"></ve-pie>
<ve-line :data="chartData2" v-else></ve-line>
```
下面是数据源格式的一个示例：
```js
chartData: {
    columns: ['time','bank1','bank2','bank3'],
    rawData: [
        { time: "2016年", bank1: "12", bank2: "13", bank3: "12" },
        { time: "2017年", bank1: "13", bank2: "23", bank3: "17" },
        { time: "2018年", bank1: "14", bank2: "33", bank3: "12" }
    ]
};
```

#### 3.2.13 错误处理模块

当发生错误时，VUE会跳转到该界面。实际上，该界面只是一个静态的界面，用于告知用户出现差错，并提供一个回到主界面的链接。如果不设置该界面，VUE会呈现一个完全空白的界面，对用户不太友好。