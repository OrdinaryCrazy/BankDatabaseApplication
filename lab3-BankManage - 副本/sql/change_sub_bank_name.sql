CREATE OR REPLACE PROCEDURE CHANGE_BANK_NAME(
    oldBankName IN  CHAR,
    newBankName IN  CHAR,
    result      OUT NUMBER
    -- debugnew    OUT CHAR,
    -- debugold    OUT CHAR
)
AS
    tempCount number;
BEGIN
    -- dbms_output.put_line(newBankName);
    -- dbms_output.put_line(oldBankName);
    -- debugnew := newBankName;
    -- debugold := oldBankName;
    SELECT COUNT(*) INTO tempCount 
    FROM DUAL 
    WHERE EXISTS(SELECT NULL FROM SUB_BANK WHERE BANK_NAME = newBankName);

    IF(tempCount > 0) THEN
        result := 1;
    ELSE
        SELECT COUNT(*) INTO tempCount 
        FROM DUAL 
        WHERE EXISTS(SELECT NULL FROM SUB_BANK WHERE BANK_NAME = oldBankName);

        IF(tempCount = 0) THEN
            result := 2;
        ELSE
            EXECUTE IMMEDIATE ' ALTER TABLE LOAN DROP 
                                CONSTRAINT FK_BANK_NAME
                                ';
            EXECUTE IMMEDIATE ' ALTER TABLE CUSTOMER_DEPOSIT_ACCOUNT 
                                DROP CONSTRAINT FK_CD_BANK_NAME
                                ';
            EXECUTE IMMEDIATE ' ALTER TABLE CUSTOMER_CHECK_ACCOUNT 
                                DROP CONSTRAINT FK_CC_BANK_NAME
                                ';
        -----------------------------------------------
            UPDATE  SUB_BANK 
            SET     BANK_NAME = newBankName
            WHERE   BANK_NAME = oldBankName;
        -----------------------------------------------
            UPDATE  LOAN 
            SET     BANK_NAME = newBankName
            WHERE   BANK_NAME = oldBankName;
        -----------------------------------------------
            UPDATE  CUSTOMER_DEPOSIT_ACCOUNT
            SET     BANK_NAME = newBankName
            WHERE   BANK_NAME = oldBankName;
        -----------------------------------------------
            UPDATE  CUSTOMER_CHECK_ACCOUNT
            SET     BANK_NAME = newBankName
            WHERE   BANK_NAME = oldBankName;
        -----------------------------------------------
            EXECUTE IMMEDIATE ' ALTER TABLE LOAN 
                                ADD CONSTRAINT FK_BANK_NAME 
                                    FOREIGN KEY(BANK_NAME)  
                                    REFERENCES SUB_BANK(BANK_NAME)
                                ';
            EXECUTE IMMEDIATE ' ALTER TABLE CUSTOMER_DEPOSIT_ACCOUNT 
                                ADD CONSTRAINT FK_CD_BANK_NAME 
                                    FOREIGN KEY(BANK_NAME)  
                                    REFERENCES SUB_BANK(BANK_NAME)
                                ';
            EXECUTE IMMEDIATE ' ALTER TABLE CUSTOMER_CHECK_ACCOUNT 
                                ADD CONSTRAINT FK_CC_BANK_NAME 
                                    FOREIGN KEY(BANK_NAME)  
                                    REFERENCES SUB_BANK(BANK_NAME)
                                ';
            result := 0;
        END IF;
    END IF;
END CHANGE_BANK_NAME;
/
-- CREATE OR REPLACE TRIGGER BANK_NAME_CHANGE
-- AFTER UPDATE ON SUB_BANK
-- FOR EACH ROW
-- BEGIN
--     IF :old.BANK_NAME IS NOT NULL AND :old.BANK_NAME != :new.BANK_NAME THEN
--     -----------------------------------------------
--         UPDATE  LOAN 
--         SET     BANK_NAME = :new.BANK_NAME 
--         WHERE   BANK_NAME = :old.BANK_NAME;
--     -----------------------------------------------
--         UPDATE  CUSTOMER_DEPOSIT_ACCOUNT
--         SET     BANK_NAME = :new.BANK_NAME 
--         WHERE   BANK_NAME = :old.BANK_NAME;
--     -----------------------------------------------
--         UPDATE  CUSTOMER_CHECK_ACCOUNT
--         SET     BANK_NAME = :new.BANK_NAME 
--         WHERE   BANK_NAME = :old.BANK_NAME;
--     -----------------------------------------------
--     END IF;
-- END;
-- /