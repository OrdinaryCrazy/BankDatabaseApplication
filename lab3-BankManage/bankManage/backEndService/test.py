from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from flask_cors import *
import json
import time




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
    custype  = request.form['custype']
    print(username)
    print(password)
    print(custype)

   
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

#==============================================================================================
# 支行管理 后台功能
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
                                            {'id':'331002199802021545','name': '张三','dept':'人事处','tel':'10086','addr':'黄山路','date_s':'2010-12-30'},
                                            {'id':'33100220001002002X','name': '李四','dept':'财务处','tel':'10010','addr':'合作化路','date_s':'2011-02-00'},
                                            {'id':'331002199011110010','name': '王五','dept':'前台','tel':'10000','addr':'肥西路','date_s':'2019-04-30'}                                        ]
                                    })
                                )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    if (rstype=="Update"):
        # Todo: 实现数据库操作，修改或新增记录
        print('Update')
        date_s=request.form['date_s']
        print(date_s)
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

@app.route('/staffCustomer',methods=['POST'])
def staffCustomer():
    rstype=request.form['type']
    # staffID=request.form['staffID'] # 员工身份证号，用于查询和修改、删除
    # custID=request.form['custID'] # 客户身份证号，用于修改、删除
    # serviceType=request.form['serviceType'] # 服务类型，用于修改
    # old_custID=request.form['old_custID'] # 旧的客户身份证号，用于修改，null代表新增
    # old_staffID=request.form['old_staffID'] # 旧的员工身份证号，用于修改
    if (rstype=="SearchByStaff"):
        # Todo: 实现数据库操作，返回查询的结果
        staffID=request.form['staffid'] # 员工身份证号，查找所有关于该员工的客户联系
        print('SearchByStaff')
        print(staffID)
        response = make_response(jsonify({    
                                        'code':200,
                                        'list':[
                                            {'id':'331002199802021545','name': '张三','type':'1'},
                                            {'id':'331002195602021545','name': '李四','type':'0'},
                                        ]
                                    })
                                )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    if (rstype=='SearchByCustomer'):
        # Todo: 实现数据库操作，返回查询的结果
        custID=request.form['custid'] # 客户身份证号，查找所有关于该客户的员工联系
        print('SearchByCustomer')
        print(custID)
        response = make_response(jsonify({    
                                        'code':200,
                                        'list':[
                                            {'staffid':'331002199802021545','staffname': '张三','type':'1'},
                                            {'staffid':'331002195602021545','staffname': '李四','type':'0'},
                                        ]
                                    })
                                )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    if (rstype=="Update"):
        # Todo: 实现数据库操作，修改或新增记录（建议使用视图）
        # 并将修改或新增的记录返回给前端（前端需要的主要是名字，但是为了兼容性，应该将整条记录都返回）
        print('Update')
        response = make_response(jsonify({    
                                        'code':200,
                                        'record': {'id':'331002199802021545','name': '张三','staffid':'331002199802021545','staffname': '李四','type':'1'}
                                        })
                                )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    if (rstype=="Delete"):
        # Todo: 实现数据库操作，删除记录
        print('Delete')
        staffID=request.form['staffid'] # 员工身份证号
        custID=request.form['custid'] # 客户身份证号，这两个主键可以用于删除联系
        print(staffID)
        print(custID)
        response = make_response(jsonify({    
                                        'code':200,
                                        'msg': 'ok'
                                        })
                                )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response

@app.route('/pay',methods=['POST'])
def pay():
    rstype=request.form['type']
    # id=request.form['loanID'] # 贷款号，用于查询和新增支付记录
    # date=request.form['date'] # 支付日期，用于新增记录
    # money=request.form['money'] # 支付金额，用于新增记录

    if (rstype=="Search"):
        # Todo: 实现数据库操作，返回查询的结果
        print('Search')
        response = make_response(jsonify({    
                                        'code':200,
                                        'list':[
                                            {'date':'2019-05-03','money':2500},
                                            {'date':'2019-05-04','money':2000},
                                            {'date':'2019-05-05','money':3000}
                                        ]
                                    })
                                )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    if (rstype=="Insert"):
        # Todo: 实现数据库操作，修改或新增记录
        print('Insert')
        response = make_response(jsonify({    
                                        'code':200,
                                        'msg': 'ok'
                                        })
                                )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response

@app.route('/accountCustomer',methods=['POST'])
def accountCustomer():   
    rstype=request.form['type']
    # id=request.form['accID'] # 账户号，用于查询和新增户主
    # bank=request.form['bank'] # 开户银行
    # ownerID=request.form['ownerID'] # 户主身份证号，用于新增记录
    print(rstype)
    if (rstype=="Search"):
        # Todo: 实现数据库操作，返回查询的结果
        print('Search')
        response = make_response(jsonify({    
                                        'code':200,
                                        'list':[
                                            {'ownerID':'11111','ownerName':'柳树'},
                                            {'ownerID':'11112','ownerName':'杨树'},
                                            {'ownerID':'11222','ownerName':'柏树'}
                                        ]
                                    })
                                )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    if (rstype=="Insert"):
        # Todo: 实现数据库操作，新增记录
        print('Insert')
        id=request.form['accID'] # 账户号，用于查询和新增户主
        bank=request.form['bank'] # 开户银行
        ownerID=request.form['ownerID'] # 户主身份证号，用于新增记录
        response = make_response(jsonify({    
                                        'code':200,
                                        'record': {'ID':id,'bank':bank,'ownerID':ownerID,'ownerName':'王五'}
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
                                            {'id':'331002199802021545','name': '张三','tel':'10086','addr':'黄山路',
                                            'name_link':'张三丰','tel_link':'112','email_link':'4323@qq.com','relation':'父子'},
                                            {'id':'331002195602021545','name': '李四','tel':'10086','addr':'黄山路',
                                            'name_link':'张三丰','tel_link':'112','email_link':'4323@qq.com','relation':'父子'},
                                            {'id':'331002199802021555','name': '王五','tel':'10086','addr':'黄山路',
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
                                            {'id': "123000",'owner': "张三，李四，王五，马云，刘强东",'bank': "合肥支行",'money':2563.00,
                                            'open_date': '2016-2-20','visit_date': '2018-5-6','type': '0','interest': 0.043,'cashtype': '1'},
                                            {'id': "123020",'owner': "刘强东",'bank': "合肥支行",'money':23563.00,
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
        ownerid=request.form['ownerid']
        print(ownerid)
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
                                            {'id': "123000",'customer': "10000 张三",'bank': "合肥支行",'amount':2563.00,'status':'0'},
                                            {'id': "123001",'customer': "10001 李四",'bank': "合肥支行",'amount':252263.00,'status':'1'},
                                            {'id': "123023",'customer': "10002 王五",'bank': "合肥支行",'amount':25.00,'status':'2'}
                                        ]
                                    })
                                )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    if (rstype=="Update"):
        # Todo: 实现数据库操作，新增记录，注意customer字段是所有贷款人的身份证号，使用英文逗号分隔，建议使用事务发放贷款
        print('Update')
        response = make_response(jsonify({    
                                        'code':200,
                                        'customer': '10000 张三\n10001 李四\n10002 王五'
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
                                        {'time':'2019','合肥支行':52,'南京支行':5,'杭州支行':52,'宁波支行':20},   
                                        {'time':'2020','南京支行':35,'上海支行':54,'杭州支行':29,'宁波支行':17}                                   
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