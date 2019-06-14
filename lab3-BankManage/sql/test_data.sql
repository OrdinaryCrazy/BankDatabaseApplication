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

--------------------------------------------------------------------------------------

--------------------------------------------------------------------------------------