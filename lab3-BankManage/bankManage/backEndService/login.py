from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from flask_cors import *
import json
import time
import cx_Oracle

app = Flask(__name__)
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

    connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
    cursor = connection.cursor()
    
    sqlcommand =    """
                    SELECT BANK_NAME AS username, BANK_PASS AS password 
                    FROM SUB_BANK
                    WHERE BANK_NAME = '""" + username + "'"

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
#==============================================================================================
# 注册 后台功能
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

@app.route('/account',methods=['POST'])
def account():
    rstype=request.form['type']
    if (rstype=="Search"):
        # Todo: 实现数据库操作，返回查询的结果
        print('Search')
        response = make_response(jsonify({    
                                        'code':200,
                                        'list':[
                                            {'ID': "123000",'owner': "张三，李四，王五，马云，刘强东",'bank': "合肥支行",'money':2563.00,
                                            'open_date': '2016-2-20','visit_date': '2018-5-6','type': '0','interest': 0.043,'cashtype': '1'},
                                            {'ID': "123020",'owner': "刘强东",'bank': "合肥支行",'money':23563.00,
                                            'open_date': '2016-2-20','visit_date': '2018-5-6','type': '1','overdraft': 25000000}
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

@app.route('/loan',methods=['POST'])
def loan():
    rstype=request.form['type']
    if (rstype=="Search"):
        # Todo: 实现数据库操作，返回查询的结果
        print('Search')
        response = make_response(jsonify({    
                                        'code':200,
                                        'list':[
                                            {'ID': "123000",'customer': "张三",'bank': "合肥支行",'amount':2563.00,'status':'1'},
                                            {'ID': "123001",'customer': "李四",'bank': "合肥支行",'amount':252263.00,'status':'0'},
                                            {'ID': "123023",'customer': "王五",'bank': "合肥支行",'amount':25.00,'status':'2'}
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

@app.route('/summary',methods=['POST'])
def summary():
    # Todo: 根据前端返回的要求，实现数据库操作，返回统计数据。另外，可以生成统计图，路径为static/summary.png，以供前端调用
    response = make_response(jsonify({    
                                    'code':200,
                                    'columnList':['合肥支行','南京支行','上海支行','杭州支行','宁波支行'],
                                    'rawData':[
                                        {'time':'2018','合肥支行':25,'南京支行':45,'上海支行':21,'杭州支行':41,'宁波支行':25},
                                        {'time':'2019','合肥支行':52,'南京支行':5,'上海支行':121,'杭州支行':52,'宁波支行':20},                                       
                                    ]
                                    })
                            )
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response



if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run()