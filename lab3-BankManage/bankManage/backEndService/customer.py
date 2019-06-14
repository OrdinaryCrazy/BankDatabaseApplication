from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from flask_cors import *
import json
import time
import cx_Oracle

from flask import Blueprint

customer_api = Blueprint('customer_api', __name__)
#==============================================================================================
# 客户管理 后台功能
@customer_api.route('/customer',methods=['POST'])
def customer():
    rstype=request.form['type']
    if (rstype=="Search"):
        # Todo: 实现数据库操作，返回查询的结果
        print('Search')

        connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
        cursor = connection.cursor()

        nameSearch      = request.form['nameSearch']
        nameSearch      = nameSearch.rstrip()
        idSearch        = request.form['idSearch']
        idSearch        = idSearch.rstrip()
        telSearch       = request.form['telSearch']
        telSearch       = telSearch.rstrip()
        addrSearch      = request.form['addrSearch']
        addrSearch      = addrSearch.rstrip()
        linknameSearch  = request.form['linknameSearch']
        linknameSearch  = linknameSearch.rstrip()
        linktelSearch   = request.form['linktelSearch']
        linktelSearch   = linktelSearch.rstrip()
        emailSearch     = request.form['emailSearch']
        emailSearch     = emailSearch.rstrip()

        sqlcommand = ""
        sqlcommand = sqlcommand + " SELECT"
        sqlcommand = sqlcommand + " CUSTOMER_ID                 AS id"          + ','
        sqlcommand = sqlcommand + " CUSTOMER_NAME               AS name "       + ','
        sqlcommand = sqlcommand + " CUSTOMER_PHONE              AS tel"         + ','
        sqlcommand = sqlcommand + " CUSTOMER_ADDRESS            AS addr"        + ','
        sqlcommand = sqlcommand + " CUSTOMER_CONTACT_NAME       AS name_link"   + ','
        sqlcommand = sqlcommand + " CUSTOMER_CONTACT_PHONE      AS tel_link"    + ','
        sqlcommand = sqlcommand + " CUSTOMER_CONTACT_EMAIL      AS email_link"  + ','
        sqlcommand = sqlcommand + " CUSTOMER_CONTACT_RELATION   AS relation"
        sqlcommand = sqlcommand + " FROM"
        sqlcommand = sqlcommand + " CUSTOMER"
        sqlcommand = sqlcommand + " WHERE"
        sqlcommand = sqlcommand + " CUSTOMER_ID IS NOT NULL"
        if (len(nameSearch) > 0) :
            sqlcommand = sqlcommand + " AND CUSTOMER_ID LIKE '%"        + nameSearch + "%'"
        if (len(idSearch) > 0) :
            sqlcommand = sqlcommand + " AND CUSTOMER_NAME LIKE '%"      + idSearch + "%'"
        if (len(telSearch) > 0) :
            sqlcommand = sqlcommand + " AND CUSTOMER_PHONE LIKE '%"     + telSearch + "%'"
        if (len(addrSearch) > 0) :
            sqlcommand = sqlcommand + " AND CUSTOMER_ADDRESS LIKE '%"   + addrSearch + "%'"
        if (len(linknameSearch) > 0) :
            sqlcommand = sqlcommand + " AND CUSTOMER_CONTACT_NAME LIKE '%"  + linknameSearch + "%'"
        if (len(linktelSearch) > 0) :
            sqlcommand = sqlcommand + " AND CUSTOMER_CONTACT_PHONE LIKE '%" + linktelSearch + "%'"
        if (len(emailSearch) > 0) :
            sqlcommand = sqlcommand + " AND CUSTOMER_CONTACT_EMAIL LIKE '%" + emailSearch + "%'"
 
        print(sqlcommand)
        cursor.execute(sqlcommand)
        # 使读取的 Oracle 数据字典化
        cursor.rowfactory = makeDictFactory(cursor)
        result = cursor.fetchall()

        response = make_response(jsonify({    
                                        'code':200,
                                        'list':result
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