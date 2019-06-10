from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from flask_cors import *
import json
import time
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


@app.route('/staff',methods=['POST'])
def staff():
    rstype=request.form['type']
    if (rstype=="Search"):
        # Todo: 实现数据库操作，返回查询的结果
        print('Search')
        response = make_response(jsonify({    
                                        'code':200,
                                        'list':[
                                            {'ID':'331002199802021545','name': '张三','dept':'人事处','tel':'10086','addr':'黄山路','date':'2010-12-30'},
                                            {'ID':'33100220001002002X','name': '李四','dept':'财务处','tel':'10010','addr':'合作化路','date':'2011-02-00'},
                                            {'ID':'331002199011110010','name': '王五','dept':'前台','tel':'10000','addr':'肥西路','date':'2019-04-30'}                                        ]
                                    })
                                )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    if (rstype=="Update"):
        # Todo: 实现数据库操作，修改或新增记录
        print('Update')
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
        print('Delete')
        response = make_response(jsonify({    
                                        'code':200,
                                        'msg': 'ok'
                                        })
                                )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response


@app.route('/customer',methods=['POST'])
def customer():
    rstype=request.form['type']
    if (rstype=="Search"):
        # Todo: 实现数据库操作，返回查询的结果
        print('Search')
        response = make_response(jsonify({    
                                        'code':200,
                                        'list':[
                                            {'ID':'331002199802021545','name': '张三','tel':'10086','addr':'黄山路',
                                            'name_link':'张三丰','tel_link':'112','email_link':'4323@qq.com','relation':'父子'},
                                            {'ID':'331002195602021545','name': '李四','tel':'10086','addr':'黄山路',
                                            'name_link':'张三丰','tel_link':'112','email_link':'4323@qq.com','relation':'父子'},
                                            {'ID':'331002199802021555','name': '王五','tel':'10086','addr':'黄山路',
                                            'name_link':'张三丰','tel_link':'112','email_link':'4323@qq.com','relation':'父子'}
                                        ]
                                    })
                                )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    if (rstype=="Update"):
        # Todo: 实现数据库操作，修改或新增记录
        print('Update')
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
        print('Delete')
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