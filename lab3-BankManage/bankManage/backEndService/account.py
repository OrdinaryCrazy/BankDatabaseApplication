from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from flask_cors import *
import json
import time
import cx_Oracle

from flask import Blueprint

account_api = Blueprint('account_api', __name__)
#==============================================================================================
# 账户管理 后台功能
@account_api.route('/account',methods=['POST'])
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
