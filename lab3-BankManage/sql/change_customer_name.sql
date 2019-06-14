CREATE OR REPLACE PROCEDURE CHANGE_CUSTOMER_NAME(
    oldBankName IN  CHAR,
    newBankName IN  CHAR,
    result      OUT NUMBER
)
AS
    tempCount number;
BEGIN
    SELECT COUNT(*) INTO tempCount 
    FROM DUAL 
    WHERE EXISTS(SELECT NULL FROM CUSTOMER WHERE CUSTOMER_ID = newBankName);

    IF(tempCount > 0) THEN
        result := 1;
    ELSE
        SELECT COUNT(*) INTO tempCount 
        FROM DUAL 
        WHERE EXISTS(SELECT NULL FROM CUSTOMER WHERE CUSTOMER_ID = oldBankName);

        IF(tempCount = 0) THEN
            result := 2;
        ELSE
            EXECUTE IMMEDIATE ' ALTER TABLE EMPLOYEE_CUSTOMER DROP 
                                CONSTRAINT FK_EC_CUSTOMER_ID
                                ';
            EXECUTE IMMEDIATE ' ALTER TABLE CUSTOMER_DEPOSIT_ACCOUNT DROP 
                                CONSTRAINT FK_CD_CUSTOMER_ID
                                ';
            EXECUTE IMMEDIATE ' ALTER TABLE CUSTOMER_CHECK_ACCOUNT DROP 
                                CONSTRAINT FK_CC_CUSTOMER_ID
                                ';
            EXECUTE IMMEDIATE ' ALTER TABLE LOAN_CUSTOMER DROP 
                                CONSTRAINT FK_LC_CUSTOMER_ID
                                ';
        -----------------------------------------------
            UPDATE  CUSTOMER 
            SET     CUSTOMER_ID = newBankName
            WHERE   CUSTOMER_ID = oldBankName;
        -----------------------------------------------
            UPDATE  EMPLOYEE_CUSTOMER 
            SET     CUSTOMER_ID = newBankName
            WHERE   CUSTOMER_ID = oldBankName;
        -----------------------------------------------
            UPDATE  CUSTOMER_DEPOSIT_ACCOUNT 
            SET     CUSTOMER_ID = newBankName
            WHERE   CUSTOMER_ID = oldBankName;
        -----------------------------------------------
            UPDATE  CUSTOMER_CHECK_ACCOUNT 
            SET     CUSTOMER_ID = newBankName
            WHERE   CUSTOMER_ID = oldBankName;
        -----------------------------------------------
            UPDATE  LOAN_CUSTOMER 
            SET     CUSTOMER_ID = newBankName
            WHERE   CUSTOMER_ID = oldBankName;
        -----------------------------------------------
            EXECUTE IMMEDIATE ' ALTER TABLE EMPLOYEE_CUSTOMER 
                                ADD CONSTRAINT FK_EC_CUSTOMER_ID 
                                    FOREIGN KEY(CUSTOMER_ID)  
                                    REFERENCES CUSTOMER(CUSTOMER_ID)
                                ';
            EXECUTE IMMEDIATE ' ALTER TABLE CUSTOMER_DEPOSIT_ACCOUNT 
                                ADD CONSTRAINT FK_CD_CUSTOMER_ID 
                                    FOREIGN KEY(CUSTOMER_ID)  
                                    REFERENCES CUSTOMER(CUSTOMER_ID)
                                ';
            EXECUTE IMMEDIATE ' ALTER TABLE CUSTOMER_CHECK_ACCOUNT 
                                ADD CONSTRAINT FK_CC_CUSTOMER_ID 
                                    FOREIGN KEY(CUSTOMER_ID)  
                                    REFERENCES CUSTOMER(CUSTOMER_ID)
                                ';
            EXECUTE IMMEDIATE ' ALTER TABLE LOAN_CUSTOMER 
                                ADD CONSTRAINT FK_LC_CUSTOMER_ID 
                                    FOREIGN KEY(CUSTOMER_ID)  
                                    REFERENCES CUSTOMER(CUSTOMER_ID)
                                ';
            result := 0;
        END IF;
    END IF;
END CHANGE_CUSTOMER_NAME;
/