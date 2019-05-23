/*==============================================================*/
/* DBMS name:      ORACLE Version 11g                           */
/* Created on:     2019/5/19 20:33:38                           */
/*==============================================================*/


alter table "CheckAccount"
   drop constraint FK_CHECKACC_ACCOUNT_C_ACCOUNT;

alter table "Customer_Check"
   drop constraint FK_CUSTOMER_CUSTOMER_CHECK;

alter table "Customer_CheckAccount"
   drop constraint FK_CUSTOMER_CHECKACCO_CHECKACC;

alter table "Customer_CheckAccount"
   drop constraint FK_CUSTOMER_SUBBANK_C_SUBBANK;

alter table "Customer_Deposit"
   drop constraint FK_CUSTOMER_CUSTOMER_DEPOSIT;

alter table "Customer_DepositAccount"
   drop constraint FK_CUSTOMER_DEPOSITAC_DEPOSITA;

alter table "Customer_DepositAccount"
   drop constraint FK_CUSTOMER_SUBBANK_D_SUBBANK;

alter table "Department"
   drop constraint FK_DEPARTME_SUBBANK_D_SUBBANK;

alter table "DepositAccount"
   drop constraint FK_DEPOSITA_ACCOUNT_D_ACCOUNT;

alter table "Employee"
   drop constraint FK_EMPLOYEE_EMPLOYEE__DEPARTME;

alter table "Employee_Customer"
   drop constraint FK_EMPLOYEE_EMPLOYEE__EMPLOYEE;

alter table "Employee_Customer"
   drop constraint FK_EMPLOYEE_EMPLOYEE__CUSTOMER;

alter table "Loan"
   drop constraint FK_LOAN_LOAN_SUBB_SUBBANK;

alter table "Loan_Customer"
   drop constraint FK_LOAN_CUS_LOAN_CUST_LOAN;

alter table "Loan_Customer"
   drop constraint FK_LOAN_CUS_LOAN_CUST_CUSTOMER;

alter table "Pay"
   drop constraint FK_PAY_LOAN_PAY_LOAN;

drop table "Account" cascade constraints;

drop table "CheckAccount" cascade constraints;

drop table "Customer" cascade constraints;

drop table "Customer_Check" cascade constraints;

drop index "CheckAccount_UPONE_FK";

drop index "SubBank_Check_FK";

drop table "Customer_CheckAccount" cascade constraints;

drop table "Customer_Deposit" cascade constraints;

drop index "DepositAccount_UPONE_FK";

drop index "SubBank_Deposit_FK";

drop table "Customer_DepositAccount" cascade constraints;

drop index "SubBank_Department_FK";

drop table "Department" cascade constraints;

drop table "DepositAccount" cascade constraints;

drop index "Employee_Department_FK";

drop table "Employee" cascade constraints;

drop index "Employee_Customer2_FK";

drop index "Employee_Customer_FK";

drop table "Employee_Customer" cascade constraints;

drop index "Loan_SubBank_FK";

drop table "Loan" cascade constraints;

drop index "Loan_Customer2_FK";

drop index "Loan_Customer_FK";

drop table "Loan_Customer" cascade constraints;

drop index "Loan_Pay_FK";

drop table "Pay" cascade constraints;

drop table "SubBank" cascade constraints;

/*==============================================================*/
/* Table: "Account"                                             */
/*==============================================================*/
create table "Account" 
(
   "Account_ID"         NUMBER(16)           not null,
   "Account_Money"      FLOAT,
   "Account_RegDate"    DATE,
   "Account_RegBank"    CHAR(50),
   constraint PK_ACCOUNT primary key ("Account_ID")
);

/*==============================================================*/
/* Table: "CheckAccount"                                        */
/*==============================================================*/
create table "CheckAccount" 
(
   "Account_ID"         NUMBER(16)           not null,
   "Account_Money"      FLOAT,
   "Account_RegDate"    DATE,
   "Account_RegBank"    CHAR(50),
   "Overdraft"          FLOAT,
   constraint PK_CHECKACCOUNT primary key ("Account_ID")
);

/*==============================================================*/
/* Table: "Customer"                                            */
/*==============================================================*/
create table "Customer" 
(
   "User_ID"            NUMBER(16)           not null,
   "User_Name"          CHAR(32),
   "User_Phone"         NUMBER(12),
   "User_Address"       CHAR(128),
   "User_Contact_Name"  CHAR(32),
   "User_Contact_Phone" NUMBER(12),
   "User_Contact_Email" CHAR(64),
   "User_Contact_Relation" CHAR(32),
   constraint PK_CUSTOMER primary key ("User_ID")
);

/*==============================================================*/
/* Table: "Customer_Check"                                      */
/*==============================================================*/
create table "Customer_Check" 
(
   "User_ID"            NUMBER(16)           not null,
   constraint PK_CUSTOMER_CHECK primary key ("User_ID")
);

/*==============================================================*/
/* Table: "Customer_CheckAccount"                               */
/*==============================================================*/
create table "Customer_CheckAccount" 
(
   "Bank_Name"          CHAR(50)             not null,
   "Account_ID"         NUMBER(16)           not null,
   "LastView_C"         DATE
);

/*==============================================================*/
/* Index: "SubBank_Check_FK"                                    */
/*==============================================================*/
create index "SubBank_Check_FK" on "Customer_CheckAccount" (
   "Bank_Name" ASC
);

/*==============================================================*/
/* Index: "CheckAccount_UPONE_FK"                               */
/*==============================================================*/
create index "CheckAccount_UPONE_FK" on "Customer_CheckAccount" (
   "Account_ID" ASC
);

/*==============================================================*/
/* Table: "Customer_Deposit"                                    */
/*==============================================================*/
create table "Customer_Deposit" 
(
   "User_ID"            NUMBER(16)           not null,
   constraint PK_CUSTOMER_DEPOSIT primary key ("User_ID")
);

/*==============================================================*/
/* Table: "Customer_DepositAccount"                             */
/*==============================================================*/
create table "Customer_DepositAccount" 
(
   "Bank_Name"          CHAR(50)             not null,
   "Account_ID"         NUMBER(16)           not null,
   "LastView_D"         DATE
);

/*==============================================================*/
/* Index: "SubBank_Deposit_FK"                                  */
/*==============================================================*/
create index "SubBank_Deposit_FK" on "Customer_DepositAccount" (
   "Bank_Name" ASC
);

/*==============================================================*/
/* Index: "DepositAccount_UPONE_FK"                             */
/*==============================================================*/
create index "DepositAccount_UPONE_FK" on "Customer_DepositAccount" (
   "Account_ID" ASC
);

/*==============================================================*/
/* Table: "Department"                                          */
/*==============================================================*/
create table "Department" 
(
   "Department_ID"      NUMBER(6)            not null,
   "Bank_Name"          CHAR(50)             not null,
   "Department_Name"    CHAR(50),
   "Department_Type"    CHAR(16),
   "Department_Leader"  NUMBER(16)           not null,
   constraint PK_DEPARTMENT primary key ("Department_ID")
);

/*==============================================================*/
/* Index: "SubBank_Department_FK"                               */
/*==============================================================*/
create index "SubBank_Department_FK" on "Department" (
   "Bank_Name" ASC
);

/*==============================================================*/
/* Table: "DepositAccount"                                      */
/*==============================================================*/
create table "DepositAccount" 
(
   "Account_ID"         NUMBER(16)           not null,
   "Account_Money"      FLOAT,
   "Account_RegDate"    DATE,
   "Account_RegBank"    CHAR(50),
   "InterestRate"       FLOAT,
   "Currencytype"       CHAR(16),
   constraint PK_DEPOSITACCOUNT primary key ("Account_ID")
);

/*==============================================================*/
/* Table: "Employee"                                            */
/*==============================================================*/
create table "Employee" 
(
   "Employee_ID"        NUMBER(16)           not null,
   "Department_ID"      NUMBER(6)            not null,
   "Employee_Name"      CHAR(32),
   "Employee_Phone"     NUMBER(12),
   "Employee_Address"   CHAR(128),
   "Employee_EnterDate" DATE,
   constraint PK_EMPLOYEE primary key ("Employee_ID")
);

/*==============================================================*/
/* Index: "Employee_Department_FK"                              */
/*==============================================================*/
create index "Employee_Department_FK" on "Employee" (
   "Department_ID" ASC
);

/*==============================================================*/
/* Table: "Employee_Customer"                                   */
/*==============================================================*/
create table "Employee_Customer" 
(
   "Employee_ID"        NUMBER(16)           not null,
   "User_ID"            NUMBER(16)           not null,
   "ServiceType"        CHAR(16),
   constraint PK_EMPLOYEE_CUSTOMER primary key ("Employee_ID", "User_ID")
);

/*==============================================================*/
/* Index: "Employee_Customer_FK"                                */
/*==============================================================*/
create index "Employee_Customer_FK" on "Employee_Customer" (
   "Employee_ID" ASC
);

/*==============================================================*/
/* Index: "Employee_Customer2_FK"                               */
/*==============================================================*/
create index "Employee_Customer2_FK" on "Employee_Customer" (
   "User_ID" ASC
);

/*==============================================================*/
/* Table: "Loan"                                                */
/*==============================================================*/
create table "Loan" 
(
   "Loan_ID"            NUMBER(16)           not null,
   "Bank_Name"          CHAR(50)             not null,
   "Loan_Money"         FLOAT,
   constraint PK_LOAN primary key ("Loan_ID")
);

/*==============================================================*/
/* Index: "Loan_SubBank_FK"                                     */
/*==============================================================*/
create index "Loan_SubBank_FK" on "Loan" (
   "Bank_Name" ASC
);

/*==============================================================*/
/* Table: "Loan_Customer"                                       */
/*==============================================================*/
create table "Loan_Customer" 
(
   "Loan_ID"            NUMBER(16)           not null,
   "User_ID"            NUMBER(16)           not null,
   constraint PK_LOAN_CUSTOMER primary key ("Loan_ID", "User_ID")
);

/*==============================================================*/
/* Index: "Loan_Customer_FK"                                    */
/*==============================================================*/
create index "Loan_Customer_FK" on "Loan_Customer" (
   "Loan_ID" ASC
);

/*==============================================================*/
/* Index: "Loan_Customer2_FK"                                   */
/*==============================================================*/
create index "Loan_Customer2_FK" on "Loan_Customer" (
   "User_ID" ASC
);

/*==============================================================*/
/* Table: "Pay"                                                 */
/*==============================================================*/
create table "Pay" 
(
   "Loan_ID"            NUMBER(16)           not null,
   "Pay_Date"           DATE,
   "Pay_Money"          FLOAT
);

/*==============================================================*/
/* Index: "Loan_Pay_FK"                                         */
/*==============================================================*/
create index "Loan_Pay_FK" on "Pay" (
   "Loan_ID" ASC
);

/*==============================================================*/
/* Table: "SubBank"                                             */
/*==============================================================*/
create table "SubBank" 
(
   "Bank_Name"          CHAR(50)             not null,
   "City"               CHAR(50),
   "Possession"         FLOAT,
   constraint PK_SUBBANK primary key ("Bank_Name")
);

alter table "CheckAccount"
   add constraint FK_CHECKACC_ACCOUNT_C_ACCOUNT foreign key ("Account_ID")
      references "Account" ("Account_ID");

alter table "Customer_Check"
   add constraint FK_CUSTOMER_CUSTOMER_CHECK foreign key ("User_ID")
      references "Customer" ("User_ID");

alter table "Customer_CheckAccount"
   add constraint FK_CUSTOMER_CHECKACCO_CHECKACC foreign key ("Account_ID")
      references "CheckAccount" ("Account_ID");

alter table "Customer_CheckAccount"
   add constraint FK_CUSTOMER_SUBBANK_C_SUBBANK foreign key ("Bank_Name")
      references "SubBank" ("Bank_Name");

alter table "Customer_Deposit"
   add constraint FK_CUSTOMER_CUSTOMER_DEPOSIT foreign key ("User_ID")
      references "Customer" ("User_ID");

alter table "Customer_DepositAccount"
   add constraint FK_CUSTOMER_DEPOSITAC_DEPOSITA foreign key ("Account_ID")
      references "DepositAccount" ("Account_ID");

alter table "Customer_DepositAccount"
   add constraint FK_CUSTOMER_SUBBANK_D_SUBBANK foreign key ("Bank_Name")
      references "SubBank" ("Bank_Name");

alter table "Department"
   add constraint FK_DEPARTME_SUBBANK_D_SUBBANK foreign key ("Bank_Name")
      references "SubBank" ("Bank_Name");

alter table "DepositAccount"
   add constraint FK_DEPOSITA_ACCOUNT_D_ACCOUNT foreign key ("Account_ID")
      references "Account" ("Account_ID");

alter table "Employee"
   add constraint FK_EMPLOYEE_EMPLOYEE__DEPARTME foreign key ("Department_ID")
      references "Department" ("Department_ID");

alter table "Employee_Customer"
   add constraint FK_EMPLOYEE_EMPLOYEE__EMPLOYEE foreign key ("Employee_ID")
      references "Employee" ("Employee_ID");

alter table "Employee_Customer"
   add constraint FK_EMPLOYEE_EMPLOYEE__CUSTOMER foreign key ("User_ID")
      references "Customer" ("User_ID");

alter table "Loan"
   add constraint FK_LOAN_LOAN_SUBB_SUBBANK foreign key ("Bank_Name")
      references "SubBank" ("Bank_Name");

alter table "Loan_Customer"
   add constraint FK_LOAN_CUS_LOAN_CUST_LOAN foreign key ("Loan_ID")
      references "Loan" ("Loan_ID");

alter table "Loan_Customer"
   add constraint FK_LOAN_CUS_LOAN_CUST_CUSTOMER foreign key ("User_ID")
      references "Customer" ("User_ID");

alter table "Pay"
   add constraint FK_PAY_LOAN_PAY_LOAN foreign key ("Loan_ID")
      references "Loan" ("Loan_ID");

