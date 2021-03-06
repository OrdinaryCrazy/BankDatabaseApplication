DROP TABLE SUB_BANK                 CASCADE CONSTRAINTS;
DROP TABLE CUSTOMER                 CASCADE CONSTRAINTS;
DROP TABLE EMPLOYEE                 CASCADE CONSTRAINTS;
DROP TABLE CHECK_ACCOUNT            CASCADE CONSTRAINTS;
DROP TABLE DEPOSIT_ACCOUNT          CASCADE CONSTRAINTS;
DROP TABLE LOAN                     CASCADE CONSTRAINTS;
DROP TABLE PAY                      CASCADE CONSTRAINTS;
DROP TABLE CUSTOMER_DEPOSIT_ACCOUNT CASCADE CONSTRAINTS;
DROP TABLE CUSTOMER_CHECK_ACCOUNT   CASCADE CONSTRAINTS;
DROP TABLE LOAN_CUSTOMER            CASCADE CONSTRAINTS;
DROP TABLE EMPLOYEE_CUSTOMER        CASCADE CONSTRAINTS;
/*==============================================================*/
/* 支行表 */
CREATE TABLE SUB_BANK (
    BANK_NAME   CHAR(50)    CONSTRAINT BAMK_PK PRIMARY KEY,
    CITY        CHAR(50),
    POSSESSION  FLOAT       DEFAULT 0.0,
------------------------------------------------
    BANK_PASS   CHAR(6)     DEFAULT '123456'
);
/*==============================================================*/
/* 用户表 */
CREATE TABLE CUSTOMER (
    CUSTOMER_ID                 NUMBER(16) CONSTRAINT CUSTOMER_PK PRIMARY KEY,
    CUSTOMER_NAME               CHAR(32),
    CUSTOMER_PHONE              NUMBER(12),
    CUSTOMER_ADDRESS            CHAR(128),
    CUSTOMER_CONTACT_NAME       CHAR(32),
    CUSTOMER_CONTACT_PHONE      NUMBER(12),
    CUSTOMER_CONTACT_EMAIL      CHAR(64),
    CUSTOMER_CONTACT_RELATION   CHAR(32),
------------------------------------------------
    CUSTOMER_PASS               CHAR(6) DEFAULT '123456'
);
/*==============================================================*/
/* 用户表 */
CREATE TABLE EMPLOYEE (
    EMPLOYEE_ID         NUMBER(16) CONSTRAINT EMPLOYEE_PK PRIMARY KEY,
    EMPLOYEE_DEPART_ID  CHAR(10),
    EMPLOYEE_BANK_NAME  CHAR(50),
    EMPLOYEE_NAME       CHAR(32),
    EMPLOYEE_PHONE      NUMBER(12),
    EMPLOYEE_ADDRESS    CHAR(128),
    EMPLOYEE_ENTERDATE  DATE,
    EMPLOYEE_LEADER     CHAR(10),  /* 不是领导就是NULL */
------------------------------------------------
    EMPLOYEE_PASS       CHAR(6)     DEFAULT '123456',
------------------------------------------------
    CONSTRAINT LEADER_UQ    UNIQUE(EMPLOYEE_LEADER)
);
/*==============================================================*/
/* 支票账户表 */
CREATE TABLE CHECK_ACCOUNT (
    CHECK_ACCOUNT_ID            NUMBER(16) CONSTRAINT CHECK_ACCOUNT_PK PRIMARY KEY,
    CHECK_ACCOUNT_MONEY         FLOAT,
    CHECK_ACCOUNT_REGDATE       DATE,
    CHECK_ACCOUNT_OVERDRAFT     FLOAT,
------------------------------------------------
    CHECK_ACCOUNT_PASS          CHAR(6) DEFAULT '123456'
);
/*==============================================================*/
/* 存储账户表 */
CREATE TABLE DEPOSIT_ACCOUNT (
    DEPOSIT_ACCOUNT_ID              NUMBER(16) CONSTRAINT DEPOSIT_ACCOUNT_PK PRIMARY KEY,
    DEPOSIT_ACCOUNT_MONEY           FLOAT,
    DEPOSIT_ACCOUNT_REGDATE         DATE,
    DEPOSIT_ACCOUNT_INTERESTRATE    FLOAT   DEFAULT 0,
    DEPOSIT_ACCOUNT_CURRENCYTYPE    NUMBER(1),
------------------------------------------------
    DEPOSIT_ACCOUNT_PASS            CHAR(6) DEFAULT '123456'
);
/*==============================================================*/
/* 贷款表 */
CREATE TABLE LOAN (
    LOAN_ID     NUMBER(16)  CONSTRAINT LOAN_PK PRIMARY KEY,
    BANK_NAME   CHAR(50),
    LOAN_MONEY  FLOAT,
    STATUS      NUMBER(1),
    CONSTRAINT FK_BANK_NAME FOREIGN KEY(BANK_NAME)  REFERENCES SUB_BANK(BANK_NAME)
);
/*==============================================================*/
/* 支付表 */
CREATE TABLE PAY (
    LOAN_ID     NUMBER(16),
    PAY_DATE    DATE,
    PAY_MONEY   FLOAT,
    CONSTRAINT FK_LOAN_ID   FOREIGN KEY(LOAN_ID)    REFERENCES LOAN(LOAN_ID)
);
/*==============================================================*/
CREATE TABLE CUSTOMER_DEPOSIT_ACCOUNT (
    BANK_NAME           CHAR(50),        /* CONSTRAINT CD_BANK_NAME_PK  PRIMARY KEY, */
    CUSTOMER_ID         NUMBER(16),     /* CONSTRAINT CD_CUSTOMER_ID   PRIMARY KEY, */
    DEPOSIT_ACCOUNT_ID  NUMBER(16),
    LAST_VIEW           DATE,
    CONSTRAINT PK_CUSTOMER_DEPOSIT_ACCOUNT  PRIMARY KEY(BANK_NAME, CUSTOMER_ID),
    CONSTRAINT FK_CD_BANK_NAME              FOREIGN KEY(BANK_NAME)          REFERENCES SUB_BANK(BANK_NAME),
    CONSTRAINT FK_CD_CUSTOMER_ID            FOREIGN KEY(CUSTOMER_ID)        REFERENCES CUSTOMER(CUSTOMER_ID),
    CONSTRAINT FK_CD_DEPOSIT_ACCOUNT_ID     FOREIGN KEY(DEPOSIT_ACCOUNT_ID) REFERENCES DEPOSIT_ACCOUNT(DEPOSIT_ACCOUNT_ID)
);
/*==============================================================*/
CREATE TABLE CUSTOMER_CHECK_ACCOUNT (
    BANK_NAME           CHAR(50),        /* CONSTRAINT CC_BANK_NAME_PK  PRIMARY KEY, */
    CUSTOMER_ID         NUMBER(16),     /* CONSTRAINT CC_CUSTOMER_ID   PRIMARY KEY, */
    CHECK_ACCOUNT_ID    NUMBER(16),
    LAST_VIEW           DATE,
    CONSTRAINT PK_CUSTOMER_CHECK_ACCOUNT    PRIMARY KEY(BANK_NAME, CUSTOMER_ID),
    CONSTRAINT FK_CC_BANK_NAME              FOREIGN KEY(BANK_NAME)          REFERENCES SUB_BANK(BANK_NAME),
    CONSTRAINT FK_CC_CUSTOMER_ID            FOREIGN KEY(CUSTOMER_ID)        REFERENCES CUSTOMER(CUSTOMER_ID),
    CONSTRAINT FK_CC_CHECK_ACCOUNT_ID       FOREIGN KEY(CHECK_ACCOUNT_ID)   REFERENCES CHECK_ACCOUNT(CHECK_ACCOUNT_ID)
);
/*==============================================================*/
CREATE TABLE LOAN_CUSTOMER (
    CUSTOMER_ID NUMBER(16), /* CONSTRAINT LC_CUSTOMER_ID_PK    PRIMARY KEY, */
    LOAN_ID     NUMBER(16),  /* CONSTRAINT LC_LOAN_ID_PK        PRIMARY KEY, */
    CONSTRAINT PK_LOAN_CUSTOMER     PRIMARY KEY(LOAN_ID, CUSTOMER_ID),
    CONSTRAINT FK_LC_CUSTOMER_ID    FOREIGN KEY(CUSTOMER_ID)    REFERENCES CUSTOMER(CUSTOMER_ID),
    CONSTRAINT FK_LC_LOAN_ID        FOREIGN KEY(LOAN_ID)        REFERENCES LOAN(LOAN_ID)
);
/*==============================================================*/
CREATE TABLE EMPLOYEE_CUSTOMER (
    CUSTOMER_ID NUMBER(16), /* CONSTRAINT EC_CUSTOMER_ID_PK    PRIMARY KEY, */
    EMPLOYEE_ID NUMBER(16), /* CONSTRAINT EC_EMPLOYEE_ID_PK    PRIMARY KEY, */
    SERVICETYPE CHAR(16),
    CONSTRAINT PK_EMPLOYEE_CUSTOMER PRIMARY KEY(EMPLOYEE_ID, CUSTOMER_ID),
    CONSTRAINT FK_EC_CUSTOMER_ID    FOREIGN KEY(CUSTOMER_ID)    REFERENCES CUSTOMER(CUSTOMER_ID),
    CONSTRAINT FK_EC_EMPLOYEE_ID    FOREIGN KEY(EMPLOYEE_ID)    REFERENCES EMPLOYEE(EMPLOYEE_ID)
);
/*==============================================================*/