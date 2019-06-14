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
        print('Search')
        # Todo: 实现数据库操作，返回查询的结果
        connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
        cursor = connection.cursor()

        nameSearch  = request.form['nameSearch']
        idSearch    = request.form['idSearch']
        bankSearch  = request.form['bankSearch']
        deptSearch  = request.form['deptSearch']
        telSearch   = request.form['telSearch']
        addrSearch  = request.form['addrSearch']
        lowerBound  = request.form['lowerBound']
        upperBound  = request.form['upperBound']
        
        sqlcommand = ""
        sqlcommand = sqlcommand + " SELECT"
        sqlcommand = sqlcommand + " EMPLOYEE_ID AS ID"          + ','
        sqlcommand = sqlcommand + " EMPLOYEE_NAME AS name"      + ','
        sqlcommand = sqlcommand + " EMPLOYEE_BANK_NAME AS bank" + ','
        sqlcommand = sqlcommand + " EMPLOYEE_DEPART_ID AS dept" + ','
        sqlcommand = sqlcommand + " EMPLOYEE_PHONE AS tel"      + ','
        sqlcommand = sqlcommand + " EMPLOYEE_ADDRESS AS addr"   + ','
        sqlcommand = sqlcommand + " EMPLOYEE_ENTERDATE AS date_s"
        sqlcommand = sqlcommand + " FROM"
        sqlcommand = sqlcommand + " EMPLOYEE"
        sqlcommand = sqlcommand + " WHERE"
        sqlcommand = sqlcommand + " EMPLOYEE_ID IS NOT NULL"
        if (len(nameSearch) > 0) :
            sqlcommand = sqlcommand + " AND EMPLOYEE_NAME LIKE '%" + nameSearch + "%'"
        if (len(idSearch) > 0) :
            sqlcommand = sqlcommand + " AND EMPLOYEE_ID LIKE '%" + idSearch + "%'"
        if (len(bankSearch) > 0) :
            sqlcommand = sqlcommand + " AND EMPLOYEE_BANK_NAME LIKE '%" + bankSearch + "%'"
        if (len(deptSearch) > 0) :
            sqlcommand = sqlcommand + " AND EMPLOYEE_DEPART_ID LIKE '%" + deptSearch + "%'"
        if (len(telSearch) > 0) :
            sqlcommand = sqlcommand + " AND EMPLOYEE_PHONE LIKE '%" + telSearch + "%'"
        if (len(addrSearch) > 0) :
            sqlcommand = sqlcommand + " AND EMPLOYEE_ADDRESS LIKE '%" + telSearch + "%'"
        if (len(lowerBound) > 0) :
            sqlcommand = sqlcommand + " AND EMPLOYEE_ENTERDATE >" + lowerBound
        if (len(upperBound) > 0) :
            sqlcommand = sqlcommand + " AND EMPLOYEE_ENTERDATE <" + upperBound

        print(sqlcommand)
        cursor.execute(sqlcommand)
        # 使读取的 Oracle 数据字典化
        cursor.rowfactory = makeDictFactory(cursor)
        result = cursor.fetchall()

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
        response = make_response(jsonify({    
                                        'code':200,
                                        'msg': 'ok'
                                        })
                                )
        response.headers['Access-Control-Allow-Origin']  = '*'
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
#==============================================================================================
# 员工客户关系查询 后台功能
@staff_api.route('/staffCustomer',methods=['POST'])
def staffCustomer():
    rstype=request.form['type']
    if (rstype=="Search"):
        # Todo: 实现数据库操作，返回查询的结果
        print('Search')
        response = make_response(jsonify({    
                                        'code':200,
                                        'list':[
                                            {'ID':'331002199802021545','name': '张三','type':'1'},
                                            {'ID':'331002195602021545','name': '李四','type':'0'},
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
#==============================================================================================
# Oracle 数据字典化函数
def makeDictFactory(cursor):
    columnNames = [d[0].lower() for d in cursor.description]
    def createRow(*args):
        return dict(zip(columnNames, args))
    return createRow