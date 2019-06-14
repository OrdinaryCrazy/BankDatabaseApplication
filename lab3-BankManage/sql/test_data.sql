INSERT 
INTO    SUB_BANK(BANK_NAME, CITY, POSSESSION) 
VALUES  ('合肥城南支行测试', '合肥', '1234.12');
---------------------------------------------------------
INSERT 
INTO    SUB_BANK(BANK_NAME, CITY, POSSESSION) 
VALUES  ('南京城北支行测试', '南京', '233.12');
---------------------------------------------------------
INSERT 
INTO    SUB_BANK(BANK_NAME, CITY, POSSESSION) 
VALUES  ('无锡城北支行测试', '无锡', '6786.12');
--------------------------------------------------------------------------------------
INSERT
INTO    EMPLOYEE(   EMPLOYEE_ID,    EMPLOYEE_NAME,      EMPLOYEE_DEPART_ID, 
                    EMPLOYEE_PHONE, EMPLOYEE_ADDRESS,   EMPLOYEE_ENTERDATE
                    )
VALUES          (   '3310021998020215',     '张三',         '000001', 
                    '10086',                '黄山路',       TO_DATE('2010-12-30','YYYY-MM-DD')
                    );
--------------------------------------------------------------------------------------
INSERT
INTO    EMPLOYEE(   EMPLOYEE_ID,    EMPLOYEE_NAME,      EMPLOYEE_DEPART_ID, 
                    EMPLOYEE_PHONE, EMPLOYEE_ADDRESS,   EMPLOYEE_ENTERDATE
                    )
VALUES          (   '3310022000100200',     '李四',         '000002',
                    '10010',                '合作化路',     TO_DATE('2011-02-01','YYYY-MM-DD')
                    );
--------------------------------------------------------------------------------------
INSERT
INTO    EMPLOYEE(   EMPLOYEE_ID,    EMPLOYEE_NAME,      EMPLOYEE_DEPART_ID, 
                    EMPLOYEE_PHONE, EMPLOYEE_ADDRESS,   EMPLOYEE_ENTERDATE
                    )
VALUES          (   '3310021990111100',     '王五',         '000003',
                    '10000',                '肥西路',       TO_DATE('2019-04-30','YYYY-MM-DD')
                    ); 
--------------------------------------------------------------------------------------
INSERT
INTO    CUSTOMER(   CUSTOMER_ID,            CUSTOMER_NAME,  CUSTOMER_PHONE,
                    CUSTOMER_ADDRESS,       CUSTOMER_CONTACT_NAME,
                    CUSTOMER_CONTACT_PHONE, CUSTOMER_CONTACT_EMAIL,
                    CUSTOMER_CONTACT_RELATION
                    )
VALUES          (   '3310021998020215',     '张三',         '10086',
                    '黄山路',               '张三丰',
                    '112',                 '4323@qq.com',
                    '父子'
                    );
--------------------------------------------------------------------------------------
INSERT
INTO    CUSTOMER(   CUSTOMER_ID,            CUSTOMER_NAME,  CUSTOMER_PHONE,
                    CUSTOMER_ADDRESS,       CUSTOMER_CONTACT_NAME,
                    CUSTOMER_CONTACT_PHONE, CUSTOMER_CONTACT_EMAIL,
                    CUSTOMER_CONTACT_RELATION
                    )
VALUES          (   '3310021988020215',     '刘强东',         '10086',
                    '黄山路',               '张三丰',
                    '112',                 '4323@qq.com',
                    '父子'
                    );
--------------------------------------------------------------------------------------
INSERT
INTO    CUSTOMER(   CUSTOMER_ID,            CUSTOMER_NAME,  CUSTOMER_PHONE,
                    CUSTOMER_ADDRESS,       CUSTOMER_CONTACT_NAME,
                    CUSTOMER_CONTACT_PHONE, CUSTOMER_CONTACT_EMAIL,
                    CUSTOMER_CONTACT_RELATION
                    )
VALUES          (   '3310021956020245',     '李四',         '10086',
                    '黄山路',               '张三丰',
                    '112',                  '4323@qq.com',
                    '父子'
                    );
--------------------------------------------------------------------------------------
INSERT
INTO    CUSTOMER(   CUSTOMER_ID,            CUSTOMER_NAME,  CUSTOMER_PHONE,
                    CUSTOMER_ADDRESS,       CUSTOMER_CONTACT_NAME,
                    CUSTOMER_CONTACT_PHONE, CUSTOMER_CONTACT_EMAIL,
                    CUSTOMER_CONTACT_RELATION
                    )
VALUES          (   '3310021998020255',     '王五',         '10086',
                    '黄山路',               '张三丰',
                    '112',                  '4323@qq.com',
                    '父子'
                    );
--------------------------------------------------------------------------------------
INSERT
INTO    EMPLOYEE_CUSTOMER(CUSTOMER_ID, EMPLOYEE_ID, SERVICETYPE)
VALUES  ('3310021998020255', '3310021990111100', '贷款经理');
--------------------------------------------------------------------------------------
INSERT
INTO    EMPLOYEE_CUSTOMER(CUSTOMER_ID, EMPLOYEE_ID, SERVICETYPE)
VALUES  ('3310021998020255', '3310022000100200', '账户经理');
--------------------------------------------------------------------------------------
INSERT
INTO    DEPOSIT_ACCOUNT(DEPOSIT_ACCOUNT_ID,             DEPOSIT_ACCOUNT_MONEY, DEPOSIT_ACCOUNT_REGDATE, 
                        DEPOSIT_ACCOUNT_INTERESTRATE,   DEPOSIT_ACCOUNT_CURRENCYTYPE)
VALUES  ('123000', 2563.00, TO_DATE('2016-02-20','YYYY-MM-DD'), 0.043, 1);

INSERT
INTO    CUSTOMER_DEPOSIT_ACCOUNT(BANK_NAME, CUSTOMER_ID, DEPOSIT_ACCOUNT_ID, LAST_VIEW)
VALUES  ('合肥城南支行测试', '3310021998020215', '123000', TO_DATE('2018-05-06','YYYY-MM-DD'));
INSERT
INTO    CUSTOMER_DEPOSIT_ACCOUNT(BANK_NAME, CUSTOMER_ID, DEPOSIT_ACCOUNT_ID, LAST_VIEW)
VALUES  ('合肥城南支行测试', '3310021988020215', '123000', TO_DATE('2018-05-06','YYYY-MM-DD'));
INSERT
INTO    CUSTOMER_DEPOSIT_ACCOUNT(BANK_NAME, CUSTOMER_ID, DEPOSIT_ACCOUNT_ID, LAST_VIEW)
VALUES  ('合肥城南支行测试', '3310021956020245', '123000', TO_DATE('2018-05-06','YYYY-MM-DD'));
INSERT
INTO    CUSTOMER_DEPOSIT_ACCOUNT(BANK_NAME, CUSTOMER_ID, DEPOSIT_ACCOUNT_ID, LAST_VIEW)
VALUES  ('合肥城南支行测试', '3310021998020255', '123000', TO_DATE('2018-05-06','YYYY-MM-DD'));
--------------------------------------------------------------------------------------
INSERT
INTO    CHECK_ACCOUNT(CHECK_ACCOUNT_ID, CHECK_ACCOUNT_MONEY, CHECK_ACCOUNT_REGDATE, CHECK_ACCOUNT_OVERDRAFT)
VALUES  ('123020', 23563.00, TO_DATE('2016-02-20','YYYY-MM-DD'), 25000000);

INSERT
INTO    CUSTOMER_CHECK_ACCOUNT(BANK_NAME, CUSTOMER_ID, CHECK_ACCOUNT_ID, LAST_VIEW)
VALUES  ('合肥城南支行测试', '3310021988020215', '123020', TO_DATE('2018-05-06','YYYY-MM-DD') );
--------------------------------------------------------------------------------------
INSERT 
INTO 	LOAN (LOAN_ID,BANK_NAME,LOAN_MONEY)
VALUES 	('111000','合肥城南支行测试',50000);

INSERT 
INTO 	LOAN (LOAN_ID,BANK_NAME,LOAN_MONEY)
VALUES 	('111001','无锡城北支行测试',30000);
--------------------------------------------------------------------------------------
INSERT
INTO 	PAY (LOAN_ID,PAY_DATE,PAY_MONEY)
VALUES 	('111000',TO_DATE('2016-02-02','YYYY-MM-DD'),30000);

INSERT
INTO 	PAY (LOAN_ID,PAY_DATE,PAY_MONEY)
VALUES 	('111001',TO_DATE('2018-03-02','YYYY-MM-DD'),10000);

INSERT
INTO 	PAY (LOAN_ID,PAY_DATE,PAY_MONEY)
VALUES 	('111001',TO_DATE('2018-03-03','YYYY-MM-DD'),20000);