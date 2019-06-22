CREATE OR REPLACE PROCEDURE CHANGE_EMPLOYEE_NAME(
    oldBankName IN  CHAR,
    newBankName IN  CHAR,
    result      OUT NUMBER
)
AS
    tempCount number;
BEGIN
    SELECT COUNT(*) INTO tempCount 
    FROM DUAL 
    WHERE EXISTS(SELECT NULL FROM EMPLOYEE WHERE EMPLOYEE_ID = newBankName);

    IF(tempCount > 0) THEN
        result := 1;
    ELSE
        SELECT COUNT(*) INTO tempCount 
        FROM DUAL 
        WHERE EXISTS(SELECT NULL FROM EMPLOYEE WHERE EMPLOYEE_ID = oldBankName);

        IF(tempCount = 0) THEN
            result := 2;
        ELSE
            EXECUTE IMMEDIATE ' ALTER TABLE EMPLOYEE_CUSTOMER DROP 
                                CONSTRAINT FK_EC_EMPLOYEE_ID
                                ';
        -----------------------------------------------
            UPDATE  EMPLOYEE 
            SET     EMPLOYEE_ID = newBankName
            WHERE   EMPLOYEE_ID = oldBankName;
        -----------------------------------------------
            UPDATE  EMPLOYEE_CUSTOMER 
            SET     EMPLOYEE_ID = newBankName
            WHERE   EMPLOYEE_ID = oldBankName;
        -----------------------------------------------
            EXECUTE IMMEDIATE ' ALTER TABLE EMPLOYEE_CUSTOMER 
                                ADD CONSTRAINT FK_EC_EMPLOYEE_ID 
                                    FOREIGN KEY(EMPLOYEE_ID)  
                                    REFERENCES EMPLOYEE(EMPLOYEE_ID)
                                ';
            result := 0;
        END IF;
    END IF;
END CHANGE_EMPLOYEE_NAME;
/