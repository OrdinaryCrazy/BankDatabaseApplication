DROP TABLE SUB_BANK     CASCADE CONSTRAINTS;
DROP TABLE DEPARTMENT   CASCADE CONSTRAINTS;
/*==============================================================*/
CREATE TABLE SUB_BANK (
    BANK_NAME   CHAR(50)    CONSTRAINT BAMK_PK PRIMARY KEY,
    CITY        CHAR(50),
    POSSESSION  FLOAT,
------------------------------------------------
    BANK_PASS   CHAR(6)
);
/*==============================================================*/
CREATE TABLE DEPARTMENT (
    DEPARTMENT_ID   NUMBER(6)   CONSTRAINT DEPARTMENT_PK PRIMARY KEY,
    DEP_BANK_NAME   CHAR(50),
------------------------------------------------
    CONSTRAINT FK_DEP_BANK_NAME FOREIGN KEY(DEP_BANK_NAME)  REFERENCES SUB_BANK(BANK_NAME)
);