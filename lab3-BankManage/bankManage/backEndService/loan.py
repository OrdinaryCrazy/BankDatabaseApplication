from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from flask_cors import *
import json
import time
import cx_Oracle

from flask import Blueprint

loan_api = Blueprint('loan_api', __name__)
#==============================================================================================
# 贷款管理 后台功能
@loan_api.route('/loan',methods=['POST'])
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
