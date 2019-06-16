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

        connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
        cursor = connection.cursor()

        bankSearch  = request.form['bankSearch']
        bankSearch  = bankSearch.rstrip()
        idSearch    = request.form['idSearch']
        idSearch    = idSearch.rstrip()
        ownerSearch = request.form['ownerSearch']
        ownerSearch = ownerSearch.rstrip()
        typeSearch  = request.form['typeSearch']
        typeSearch  = typeSearch.rstrip()
        money_lo    = request.form['money_lo']
        money_lo    = money_lo.rstrip()
        money_up    = request.form['money_up']
        money_up    = money_up.rstrip()
        open_lo     = request.form['open_lo']
        open_lo     = open_lo.rstrip()
        open_up     = request.form['open_up']
        open_up     = open_up.rstrip()
        visit_lo    = request.form['visit_lo']
        visit_lo    = visit_lo.rstrip()
        visit_up    = visit_up.form['visit_up']
        visit_up    = visit_up.rstrip()

        checkresult = []
        depositresult = []

        if typeSearch == "any" or typeSearch == "check" :
            sqlcommand = ""
            sqlcommand = sqlcommand + " SELECT"
            sqlcommand = sqlcommand + " AS id"
            sqlcommand = sqlcommand + " AS owner"
            sqlcommand = sqlcommand + " AS bank"
            sqlcommand = sqlcommand + " AS money"
            sqlcommand = sqlcommand + " AS open_date"
            sqlcommand = sqlcommand + " AS visit_date"
            sqlcommand = sqlcommand + " FROM"
            sqlcommand = sqlcommand + " CHECK_ACCOUNT,"
            sqlcommand = sqlcommand + " CUSTOMER_CHECK_ACCOUNT,"
            sqlcommand = sqlcommand + " CUSTOMER,"
            print(sqlcommand)
            cursor.execute(sqlcommand)
            cursor.rowfactory = makeDictFactory(cursor)
            checkresult = cursor.fetchall()
            # for line in 

        if typeSearch == "any" or typeSearch == "saving" :
            sqlcommand = ""
            sqlcommand = sqlcommand + " SELECT"
            sqlcommand = sqlcommand + " "
            sqlcommand = sqlcommand + " "
            sqlcommand = sqlcommand + " "
            sqlcommand = sqlcommand + " FROM"
            sqlcommand = sqlcommand + " DEPOSIT_ACCOUNT,"
            sqlcommand = sqlcommand + " CUSTOMER_DEPOSIT_ACCOUNT,"
            sqlcommand = sqlcommand + " CUSTOMER,"
            print(sqlcommand)
            cursor.execute(sqlcommand)
            cursor.rowfactory = makeDictFactory(cursor)
            depositresult = cursor.fetchall()

        result = checkresult + depositresult

        if result :
            response = make_response(jsonify({    
                                            'code':200,
                                            'list':result
                                        })
                                    )
            response.headers['Access-Control-Allow-Origin']  = '*'
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
        response.headers['Access-Control-Allow-Origin']  = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response

    if (rstype=="Update"):
        # Todo: 实现数据库操作，修改或新增记录
        print('Update')

        connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
        cursor = connection.cursor()

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

        connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
        cursor = connection.cursor()

        response = make_response(jsonify({    
                                        'code':200,
                                        'msg': 'ok'
                                        })
                                )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
#==============================================================================================
# Oracle 数据字典化函数
def makeDictFactory(cursor):
    columnNames = [d[0].lower() for d in cursor.description]
    def createRow(*args):
        return dict(zip(columnNames, args))
    return createRow