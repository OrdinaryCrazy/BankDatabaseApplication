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
    username     = request.form['username']
    password     = request.form['password']
    account_type = request.form['type']
    print(username)
    print(password)
    print(account_type)
    # ToDo: 实现数据库操作,并丰富响应报文类型，如用户名已存在，或者其他错误

    connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
    cursor = connection.cursor()
    sqlcommand = ""
    if account_type == "SUB_BANK" :
        insert = "(" + "'" + username + "'" + ','  + "'" + password + "'" + ")"
        sqlcommand =    """
                        INSERT INTO 
                            SUB_BANK(BANK_NAME, BANK_PASS)
                        VALUES """ + insert
    elif account_type == "EMPLOYEE":
        insert = "(" + "'" + username + "'" + ','  + "'" + password + "'" + ")"
        sqlcommand =    """
                        INSERT INTO 
                            EMPLOYEE(EMPLOYEE_ID, EMPLOYEE_PASS)
                        VALUES """ + insert
    else :
        insert = "(" + "'" + username + "'" + ','  + "'" + password + "'" + ")"
        sqlcommand =    """
                        INSERT INTO 
                            CUSTOMER(CUSTOMER_ID, CUSTOMER_PASS)
                        VALUES """ + insert
    print(sqlcommand)
    try :
        cursor.execute(sqlcommand)
    except :
        cursor.close()
        connection.close()
        response = make_response(jsonify({    
                                            'code':500, 
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