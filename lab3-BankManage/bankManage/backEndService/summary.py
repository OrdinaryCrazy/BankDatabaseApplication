from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from flask_cors import *
import json
import time
import cx_Oracle

from flask import Blueprint

summary_api = Blueprint('summary_api', __name__)
#==============================================================================================
# 业务统计 后台功能
@summary_api.route('/summary',methods=['POST'])
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

