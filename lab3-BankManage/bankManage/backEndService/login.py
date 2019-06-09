from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from flask_cors import *
import json
# import cx_Oracle

app = Flask(__name__)
CORS(app, supports_credentials=True)

def makeDictFactory(cursor):
    columnNames = [d[0].lower() for d in cursor.description]
    def createRow(*args):
        return dict(zip(columnNames, args))
    return createRow


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # print(username)
    # print(password)
    # connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
    # cursor = connection.cursor()
    
    # sqlcommand =    """
                    # SELECT BANK_NAME AS username, BANK_PASS AS password 
                    # FROM SUB_BANK
                    # WHERE BANK_NAME = '""" + username + "'"
    # print(sqlcommand)
    # cursor.execute(sqlcommand)
    # cursor.rowfactory = makeDictFactory(cursor)
    # result = cursor.fetchone()
    # print(result)

    # cursor.close()
    # connection.close()
    if (1==1):
    # if result and result['password'][:len(password)] == password:
        response = make_response(jsonify({    
                                            'code':200,
                                            'msg':'get',
                                            'token':username
                                        })
                                    )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    response = make_response(jsonify({    
                                        'code':400,
                                        'msg':'error'
                                    })
                                )
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response



@app.route('/register',methods=['POST','OPTIONS'])
def register():
    username=request.form['username']
    password=request.form['password']
    account_type=request.form['type']
    print(username)
    print(password)
    print(account_type)
    # ToDo: 实现数据库操作,并丰富响应报文类型，如用户名已存在，或者其他错误
    response = make_response(jsonify({    
                                        'code':200,
                                        'msg':'ok'
                                    })
                                )
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

@app.route('/bank',methods=['POST'])
def bank():
    rstype=request.form['type']
    if (rstype=="Search"):
        # Todo: 实现数据库操作，返回查询的结果
        response = make_response(jsonify({    
                                        'code':200,
                                        'list':[
                                            {'name': '合肥城南支行','city': '合肥','money': 100000000},
                                            {'name': '南京城北支行','city': '南京','money': 102500000},
                                            {'name': '无锡城北支行','city': '无锡','money': 1000}
                                        ]
                                    })
                                )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    if (rstype=="Update"):
        # Todo: 实现数据库操作，修改或新增记录
        response = make_response(jsonify({    
                                        'code':200,
                                        'msg': 'ok'
                                        })
                                )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    if (rstype=="Delete"):
        # Todo: 实现数据库操作，删除记录
        response = make_response(jsonify({    
                                        'code':200,
                                        'msg': 'ok'
                                        })
                                )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response




if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run()