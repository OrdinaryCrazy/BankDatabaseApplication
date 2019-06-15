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
        visit_up    = request.form['visit_up']
        visit_up    = visit_up.rstrip()

        checkresult = []
        depositresult = []

        if typeSearch == "any" or typeSearch == "check" :
            sqlcommand = ""
            sqlcommand = sqlcommand + " SELECT"
            sqlcommand = sqlcommand + " CHECK_ACCOUNT.CHECK_ACCOUNT_ID AS id"               + ','
            # sqlcommand = sqlcommand + " AS owner" + ','
            sqlcommand = sqlcommand + " CUSTOMER_CHECK_ACCOUNT.BANK_NAME AS bank"           + ','
            sqlcommand = sqlcommand + " CHECK_ACCOUNT.CHECK_ACCOUNT_MONEY AS money"         + ','
            sqlcommand = sqlcommand + " CHECK_ACCOUNT.CHECK_ACCOUNT_REGDATE AS open_date"   + ','
            # sqlcommand = sqlcommand + " AS visit_date" + ','
            # sqlcommand = sqlcommand + " AS type" + ','
            # sqlcommand = sqlcommand + " AS interest" + ','
            # sqlcommand = sqlcommand + " AS cashtype" + ','
            sqlcommand = sqlcommand + " CHECK_ACCOUNT.CHECK_ACCOUNT_OVERDRAFT AS overdraft"
            sqlcommand = sqlcommand + " FROM"
            sqlcommand = sqlcommand + " CHECK_ACCOUNT,"
            sqlcommand = sqlcommand + " CUSTOMER,"
            sqlcommand = sqlcommand + " CUSTOMER_CHECK_ACCOUNT"
            sqlcommand = sqlcommand + " WHERE"
            sqlcommand = sqlcommand + " CHECK_ACCOUNT.CHECK_ACCOUNT_ID = CUSTOMER_CHECK_ACCOUNT.CHECK_ACCOUNT_ID"
            sqlcommand = sqlcommand + " AND CUSTOMER.CUSTOMER_ID = CUSTOMER_CHECK_ACCOUNT.CUSTOMER_ID"
            if (len(bankSearch) > 0) :
                sqlcommand = sqlcommand + " AND CUSTOMER_CHECK_ACCOUNT.BANK_NAME LIKE '%" + bankSearch + "%'"
            if (len(idSearch) > 0) :
                sqlcommand = sqlcommand + " AND CHECK_ACCOUNT.CHECK_ACCOUNT_ID LIKE '%" + idSearch + "%'"
            if (len(ownerSearch) > 0) :
                sqlcommand = sqlcommand + " AND CUSTOMER.CUSTOMER_NAME LIKE '%" + ownerSearch + "%'"
            if (len(money_lo) > 0) :
                sqlcommand = sqlcommand + " AND CHECK_ACCOUNT.CHECK_ACCOUNT_MONEY > " + money_lo
            if (len(money_up) > 0) :
                sqlcommand = sqlcommand + " AND CHECK_ACCOUNT.CHECK_ACCOUNT_MONEY < " + money_up
            if (len(open_lo) > 0) :
                sqlcommand = sqlcommand + " AND CHECK_ACCOUNT.CHECK_ACCOUNT_REGDATE > TO_DATE('" + open_lo + "','YYYY-MM-DD')"
            if (len(open_up) > 0) :
                sqlcommand = sqlcommand + " AND CHECK_ACCOUNT.CHECK_ACCOUNT_REGDATE < TO_DATE('" + open_up + "','YYYY-MM-DD')"

            print(sqlcommand)
            cursor.execute(sqlcommand)
            cursor.rowfactory = makeDictFactory(cursor)
            checkresult = cursor.fetchall()
            checkresult = [dict(t) for t in set([tuple(d.items()) for d in checkresult])]
            for line in checkresult :
                line['type'] = "0"
                line['open_date']  = line['open_date'].strftime('%Y-%m-%d')

        if typeSearch == "any" or typeSearch == "saving" :
            sqlcommand = ""
            sqlcommand = sqlcommand + " SELECT"
            sqlcommand = sqlcommand + " DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_ID AS id"               + ','
            # sqlcommand = sqlcommand + " AS owner" + ','
            sqlcommand = sqlcommand + " CUSTOMER_DEPOSIT_ACCOUNT.BANK_NAME AS bank"             + ','
            sqlcommand = sqlcommand + " DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_MONEY AS money"         + ','
            sqlcommand = sqlcommand + " DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_REGDATE AS open_date"   + ','
            # sqlcommand = sqlcommand + " AS visit_date" + ','
            # sqlcommand = sqlcommand + " AS type" + ','
            # sqlcommand = sqlcommand + " AS interest" + ','
            # sqlcommand = sqlcommand + " AS cashtype" + ','
            sqlcommand = sqlcommand + " DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_INTERESTRATE AS interest"   + ','
            sqlcommand = sqlcommand + " DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_CURRENCYTYPE AS cashtype"
            sqlcommand = sqlcommand + " FROM"
            sqlcommand = sqlcommand + " DEPOSIT_ACCOUNT,"
            sqlcommand = sqlcommand + " CUSTOMER,"
            sqlcommand = sqlcommand + " CUSTOMER_DEPOSIT_ACCOUNT"
            sqlcommand = sqlcommand + " WHERE"
            sqlcommand = sqlcommand + " DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_ID = CUSTOMER_DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_ID"
            sqlcommand = sqlcommand + " AND CUSTOMER.CUSTOMER_ID = CUSTOMER_DEPOSIT_ACCOUNT.CUSTOMER_ID"
            if (len(bankSearch) > 0) :
                sqlcommand = sqlcommand + " AND CUSTOMER_DEPOSIT_ACCOUNT.BANK_NAME LIKE '%" + bankSearch + "%'"
            if (len(idSearch) > 0) :
                sqlcommand = sqlcommand + " AND DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_ID LIKE '%" + idSearch + "%'"
            if (len(ownerSearch) > 0) :
                sqlcommand = sqlcommand + " AND CUSTOMER.CUSTOMER_NAME LIKE '%" + ownerSearch + "%'"
            if (len(money_lo) > 0) :
                sqlcommand = sqlcommand + " AND DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_MONEY > " + money_lo
            if (len(money_up) > 0) :
                sqlcommand = sqlcommand + " AND DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_MONEY < " + money_up
            if (len(open_lo) > 0) :
                sqlcommand = sqlcommand + " AND DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_REGDATE > TO_DATE('" + open_lo + "','YYYY-MM-DD')"
            if (len(open_up) > 0) :
                sqlcommand = sqlcommand + " AND DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_REGDATE < TO_DATE('" + open_up + "','YYYY-MM-DD')"

            print(sqlcommand)
            cursor.execute(sqlcommand)
            cursor.rowfactory = makeDictFactory(cursor)
            depositresult = cursor.fetchall()
            depositresult = [dict(t) for t in set([tuple(d.items()) for d in depositresult])]
            for line in depositresult :
                line['type'] = "1"
                line['cashtype'] = str(line['cashtype'])
                line['open_date']  = line['open_date'].strftime('%Y-%m-%d')

        result = checkresult + depositresult
        print(result)

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
#==============================================================================================
# Oracle 数据字典化函数
def makeDictFactory(cursor):
    columnNames = [d[0].lower() for d in cursor.description]
    def createRow(*args):
        return dict(zip(columnNames, args))
    return createRow