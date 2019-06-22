from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from flask_cors import *
import json
import time
import cx_Oracle

from register   import register_api
from bank       import bank_api
from staff      import staff_api
from summary    import summary_api
from loan       import loan_api
from customer   import customer_api
from account    import account_api

app = Flask(__name__)
app.register_blueprint(register_api)
app.register_blueprint(bank_api)
app.register_blueprint(staff_api)
app.register_blueprint(summary_api)
app.register_blueprint(loan_api)
app.register_blueprint(customer_api)
app.register_blueprint(account_api)

CORS(app, supports_credentials=True)
#==============================================================================================
# Oracle 数据字典化函数
def makeDictFactory(cursor):
    columnNames = [d[0].lower() for d in cursor.description]
    def createRow(*args):
        return dict(zip(columnNames, args))
    return createRow
#==============================================================================================
# 登录 后台功能
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    custype  = request.form['custype']
    print(username)
    print(password)
    print(custype)

    connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
    cursor = connection.cursor()
    sqlcommand = ""
    if custype == "SUB_BANK" :
        sqlcommand =    """
                        SELECT BANK_NAME AS username, BANK_PASS AS password 
                        FROM SUB_BANK
                        WHERE BANK_NAME = '""" + username + "'"
    elif custype == "EMPLOYEE":
        sqlcommand =    """
                        SELECT EMPLOYEE_ID AS username, EMPLOYEE_PASS AS password 
                        FROM EMPLOYEE
                        WHERE EMPLOYEE_ID = '""" + username + "'"
    else :
        sqlcommand =    """
                        SELECT CUSTOMER_ID AS username, CUSTOMER_PASS AS password 
                        FROM CUSTOMER
                        WHERE CUSTOMER_ID = '""" + username + "'"
    print(sqlcommand)
    cursor.execute(sqlcommand)
    # 使读取的 Oracle 数据字典化
    cursor.rowfactory = makeDictFactory(cursor)
    result = cursor.fetchone()


    cursor.close()
    connection.close()
    # 登录成功
    if result and len(password) > 0 and result['password'][:len(password)] == password :
        # print("登录成功")
        response = make_response(jsonify({    
                                            'code':200,
                                            'msg':'get',
                                            'token':username
                                        })
                                    )
        response.headers['Access-Control-Allow-Origin']  = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    # 登陆失败
    response = make_response(jsonify({    
                                        'code':400,
                                        'msg':'error'
                                    })
                                )
    response.headers['Access-Control-Allow-Origin']  = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run()