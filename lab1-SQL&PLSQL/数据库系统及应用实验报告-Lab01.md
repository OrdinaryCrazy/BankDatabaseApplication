# 数据库系统及应用实验报告-Lab01

## 实验内容

设某图书馆数据库包含下面的基本表：

*   `Book(ID: char(8)，name:varchar2(10)，author:varchar2(10)，price:float， status: int)`
    1.  图书号(`ID`)为主键，书名不能为空。
    2.  状态(`status`)为 1 表示书被借出，0 表示在馆，默认值为 0。
*   `Reader(ID:char(8)，name:varchar2(10)，age:int，address:varchar2(20))` 
    1.  读者号 ID 为主键。
*   `Borrow(book_ID:char(8)，Reader_ID:char(8)，Brrrow_Date:date，Return_Date:date)`
    1.  还期`Return_Date`为NULL表示该书未还
    2.  主键为（图书号，读者号）
    3.  图书号为外键，引用图书表的图书号
    4.  读者号为外键，引用读者表的读者号

## 实验步骤与结果

### Step 1：创建上述基本表，并插入部分测试数据

#### 创建基本表：

```plsql
/*=== 清除原有表格对象 ===*/
Drop Table Book		Cascade Constraints;
Drop Table Reader	Cascade Constraints;
Drop Table Borrow	Cascade Constraints;
/*=== 创建基本表 ===*/
/*====================================================================================*/
create table Book(
    ID      char(8)     Constraint Book_PK Primary Key,   -- 图书号
    name    varchar2(8)	NOT NULL ,                    	  -- 书名      
    author  varchar2(8),
    price   float,
    /* 状态，status = 1 表示书被借出，status = 0 表示在馆，默认值为0 */
    status  int DEFAULT 0,
    -------------------------------------------------------------
    Constraint status_Choise    Check (status = 1 or status = 0),
    Constraint price_floor      Check (price >= 0)
);
/*====================================================================================*/
create table Reader(
    ID       char(8)     Constraint Reader_PK Primary Key,  --读者号
    name     varchar2(10),
    age      int,
    address  varchar2(20),
    ----------------------------------------------------------------
    Constraint age_floor    Check (age > 0)
);
/*====================================================================================*/
create table Borrow(
    book_ID		char(8),
    Reader_ID   char(8),
    Borrow_Date	date,
    Return_Date	date,
    Constraint FK_book_ID 	Foreign Key(book_ID) 	References Book(ID),
    Constraint FK_Reader_ID	Foreign	Key(Reader_ID)	References Reader(ID),
    Constraint Borrow_PK	Primary	Key(book_ID,Reader_ID)
);
```

#### 加入测试数据

```plsql
/*====================================================================================*/
/*=== 插入数据简单测试 ===*/
/*=== 避免了执行多个SQL语句多次连接数据库的开销 ====*/
insert all
------------------------------------------------------------------------------------------------
into    Book(ID, name, author, price, status)	values  ('0001','database','C.J.Date',23.33,0)
into    Book(ID, name, author, price, status)	values  ('0002','datastru','mjh',6.66,1)
into    Book(ID, name, author, price, status)	values  ('0003','algorith','gnj',99.99,0)
------------------------------------------------------------------------------------------------
into    Reader(ID, name, age, address)  values  ('PB1485','zjt',18,'x4-414')
into    Reader(ID, name, age, address)  values  ('PB1666','dalao1',28,'d333-222')
into    Reader(ID, name, age, address)  values  ('PB4554','dalao2',44,'x5-233')
------------------------------------------------------------------------------------------------
into    Borrow(book_ID, Reader_ID, Borrow_Date, Return_Date)    values  ('0002','PB1485',to_date('04/13/2019','mm/dd/yyyy'),NULL)
------------------------------------------------------------------------------------------------
select 1 from DUAL;
/*====================================================================================*/
```



#### 简单测试

```plsql
/*====================================================================================*/
select Book.Name, Reader.Name,Borrow.Borrow_Date
from Book, Reader, Borrow
where
Book.Id = Borrow.Book_Id and
Reader.Id = Borrow.Reader_Id;
/*====================================================================================*/
```



### Step 2：设计例子，验证实体完整性、参照完整性、用户自定义完整性

`insert into Book(ID, name, author, price, status)   values (NULL,'database','C.J.Date',23.33,0);`

报错：`ORA-01400: 无法将 NULL 插入 ("SYSTEM"."BOOK"."ID")`

`insert into Reader(ID, name, age, address)          values (NULL,'lala',88，'x3-333');`

报错：`ORA-01400: 无法将 NULL 插入 ("SYSTEM"."READER"."ID")`



### Step 3：SQL语言完成下面小题，并测试运行结果

```plsql

```



### Step 4：设计存储过程，实现对 Book 表的 ID的修改

```plsql

```



### Step 5：设计触发器

>   **实现：**
>
>  * **当一本书被借出时，自动将 Book 表中相应图书的 status 修改为 1；**
>  * **当某本书被归还时，自动将 Book 表中相应图书的 status 修改为 0。**

```plsql

```



