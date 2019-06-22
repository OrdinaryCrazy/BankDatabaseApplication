from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from flask_cors import *
import json
import time
import cx_Oracle

from flask import Blueprint

register_api = Blueprint('register_api', __name__)

#==============================================================================================
# 注册 后台功能
@register_api.route('/register',methods=['POST','OPTIONS'])
def register():
    # username     = request.form['username']
    # password     = request.form['password']
    # account_type = request.form['type']
    username        = request.form['username'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
    password        = request.form['password'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
    account_type    = request.form['type'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
    city            = request.form['city'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
    money           = request.form['money'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
    name            = request.form['name'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
    tel             = request.form['tel'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
    addr            = request.form['addr'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
    name_link       = request.form['name_link'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
    tel_link        = request.form['tel_link'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
    email_link      = request.form['email_link'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
    relation        = request.form['relation'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
    dept            = request.form['dept'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
    date_s          = request.form['date_s'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
    bankname        = request.form['bankname'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  

    print(username)
    print(password)
    print(account_type)
    # ToDo: 实现数据库操作,并丰富响应报文类型，如用户名已存在，或者其他错误

    connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
    cursor = connection.cursor()
    sqlcommand = ""
    if account_type == "SUB_BANK" :
        insert = "(" + "'" + username + "'" + ','  + "'" + password + "', "
        insert = insert + "'" + city    + "', "
        insert = insert + "'" + money   + "'"
        insert = insert + ")"
        sqlcommand =    """
                        INSERT INTO 
                            SUB_BANK(BANK_NAME, BANK_PASS, CITY, POSSESSION)
                        VALUES """ + insert
    elif account_type == "EMPLOYEE":
        insert = "(" + "'" + username + "'" + ','  + "'" + password + "', " 
        insert = insert + "'" + name        + "', " 
        insert = insert + "'" + dept        + "', " 
        insert = insert + "'" + tel         + "', " 
        insert = insert + "'" + addr        + "', " 
        insert = insert + "'" + bankname    + "', " 
        insert = insert + "TO_DATE('" + date_s + "','YYYY-MM-DD')"
        insert = insert + ")"
        sqlcommand =    """
                        INSERT INTO 
                            EMPLOYEE(   EMPLOYEE_ID,        EMPLOYEE_PASS,  EMPLOYEE_NAME,
                                        EMPLOYEE_DEPART_ID, EMPLOYEE_PHONE, EMPLOYEE_ADDRESS,
                                        EMPLOYEE_BANK_NAME, EMPLOYEE_ENTERDATE
                                        )
                        VALUES """ + insert
    else :
        insert = "(" + "'" + username + "'" + ','  + "'" + password + "', "
        insert = insert + "'" + name        + "', " 
        insert = insert + "'" + tel         + "', " 
        insert = insert + "'" + addr        + "', " 
        insert = insert + "'" + name_link   + "', " 
        insert = insert + "'" + tel_link    + "', " 
        insert = insert + "'" + email_link  + "', " 
        insert = insert + "'" + relation    + "'" 
        insert = insert + ")"
        sqlcommand =    """
                        INSERT INTO 
                            CUSTOMER(   CUSTOMER_ID,    CUSTOMER_PASS,      CUSTOMER_NAME,
                                        CUSTOMER_PHONE, CUSTOMER_ADDRESS,
                                        CUSTOMER_CONTACT_NAME,  CUSTOMER_CONTACT_PHONE,
                                        CUSTOMER_CONTACT_EMAIL, CUSTOMER_CONTACT_RELATION
                                )   
                        VALUES """ + insert
    print(sqlcommand)
    try :
        cursor.execute(sqlcommand)
    except :
        print("数据库操作失败")
        cursor.close()
        connection.close()
        response = make_response(jsonify({    
                                            'code':400, 
                                            # 数据库操作失败
                                            'msg':'ok'
                                        })
                                    )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response

    cursor.close()
#===============================
    connection.commit()
#===============================
    connection.close()

    response = make_response(jsonify({    
                                        'code':200,
                                        'msg':'ok'
                                    })
                                )
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response