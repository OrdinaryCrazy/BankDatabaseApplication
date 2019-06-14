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
# Oracle 数据字典化函数
def makeDictFactory(cursor):
    columnNames = [d[0].lower() for d in cursor.description]
    def createRow(*args):
        return dict(zip(columnNames, args))
    return createRow
#==============================================================================================
# 业务统计 后台功能
@summary_api.route('/summary',methods=['POST'])
def summary():
    # Todo: 根据前端返回的要求，实现数据库操作，返回统计数据。另外，可以生成统计图，路径为static/summary.png，以供前端调用
    
    connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
    cursor = connection.cursor()


    lowerBound  = request.form['lowerBound']
    upperBound  = request.form['upperBound']
    timegrain = request.form['timegrain']
    sumtype = request.form['sumtype']
    datatype = request.form['datatype']
    graphtype = request.form['graphtype']

#####按支行统计#######饼图######

    if graphtype == 'pie':
        if datatype == 'money':#业务总金额
            if sumtype == 'saving':#存储业务
#
# 支行1     支行2      支行3
# ￥233     ￥345     ￥678 （支票账户）
#
                #check account
                sqlcommand = ""
                sqlcommand = sqlcommand + " SELECT"
                sqlcommand = sqlcommand + " BANK_NAME AS B_name1" + ','
                sqlcommand = sqlcommand + " SUM(CHECK_ACCOUNT_MONEY) AS SUM_C_A_money"
                sqlcommand = sqlcommand + " FROM"

                sqlcommand = sqlcommand + "("
                sqlcommand = sqlcommand + " SELECT"
                sqlcommand = sqlcommand + " BANK_NAME AS B_name"   + ','
                sqlcommand = sqlcommand + " CHECK_ACCOUNT_ID AS C_A_ID1"   + ','
                sqlcommand = sqlcommand + " CHECK_ACCOUNT_MONEY AS C_A_money1"
                sqlcommand = sqlcommand + " FROM"
                sqlcommand = sqlcommand + "("
                sqlcommand = sqlcommand + " SELECT"
                sqlcommand = sqlcommand + " CHECK_ACCOUNT_ID AS C_A_ID"   + ','
                sqlcommand = sqlcommand + " CHECK_ACCOUNT_MONEY AS C_A_money"
                sqlcommand = sqlcommand + " FROM"
                sqlcommand = sqlcommand + " CHECK_ACCOUNT"
                sqlcommand = sqlcommand + " WHERE"  
                if (len(lowerBound) > 0) :
                    sqlcommand = sqlcommand + " AND CHECK_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                if (len(upperBound) > 0) :
                    sqlcommand = sqlcommand + " AND CHECK_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                sqlcommand = sqlcommand + ")"
                sqlcommand = sqlcommand + "NEW_CHECK_ACCOUNT" + ','
                sqlcommand = sqlcommand + " CUSTOMER_CHECK_ACCOUNT"
                sqlcommand = sqlcommand + " WHERE" 
                sqlcommand = sqlcommand + " NEW_CHECK_ACCOUNT.CHECK_ACCOUNT_ID == CUSTOMER_CHECK_ACCOUNT.CHECK_ACCOUNT_ID" 
                sqlcommand = sqlcommand + ")"

                sqlcommand = sqlcommand + " GROUP BY"
                sqlcommand = sqlcommand + " BANK_NAME"

                print(sqlcommand)
                cursor.execute(sqlcommand)
                cursor.rowfactory = makeDictFactory(cursor)
                result = cursor.fetchall()
                for i in len(result):
                    for j in result[i]:
                        print(repr(result[i][j]),end = ',')
                    print('\n')
                        
                if result :
                    response = make_response(
                        jsonify(
                            {
                                'code': 200,
                                'list': result
                            }
                        )
                    )
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
                    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
                    return response

                response = make_response(
                jsonify(
                    {
                        'code': 400
                    }
                )
                )      
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
                response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
                return response




                #response = make_response(jsonify({    
                #                                'code':200,
                #                                'columnList':['合肥支行','南京支行','上海支行','杭州支行','宁波支行'],
                #                                'rawData':[
                #                                    {'time':'2018','合肥支行':25,'南京支行':45,'上海支行':21,'杭州支行':41,'宁波支行':25},
                #                                    {'time':'2019','合肥支行':52,'南京支行':5,'上海支行':121,'杭州支行':52,'宁波支行':20},                                       
                #                                ]
                #                                })
                #                        )
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

