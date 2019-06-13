from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from flask_cors import *
import json
import time
import cx_Oracle

from flask import Blueprint

staff_api = Blueprint('staff_api', __name__)

#==============================================================================================
# 员工管理 后台功能
@staff_api.route('/staff',methods=['POST'])
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
