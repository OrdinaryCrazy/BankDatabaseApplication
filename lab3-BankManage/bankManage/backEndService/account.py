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
        bankSearch  = bankSearch.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        idSearch    = request.form['idSearch']
        idSearch    = idSearch.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        ownerSearch = request.form['ownerSearch']
        ownerSearch = ownerSearch.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        typeSearch  = request.form['typeSearch']
        typeSearch  = typeSearch.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        money_lo    = request.form['money_lo']
        money_lo    = money_lo.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        money_up    = request.form['money_up']
        money_up    = money_up.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        open_lo     = request.form['open_lo']
        open_lo     = open_lo.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        open_up     = request.form['open_up']
        open_up     = open_up.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        visit_lo    = request.form['visit_lo']
        visit_lo    = visit_lo.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        visit_up    = request.form['visit_up']
        visit_up    = visit_up.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')

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
                line['type'] = "1"
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
                line['type'] = "0"
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

        id_s        = request.form['id']
        money       = request.form['money']
        acctype     = request.form['acctype']
        interest    = request.form['interest']
        overdraft   = request.form['overdraft']
        old_primary = request.form['old_primary']
        open_date   = request.form['open_date']
        cashtype    = request.form['cashtype']
        bank        = request.form['bank']
        ownerid     = request.form['ownerid']
        overdraft   = request.form['overdraft']

        id_s        = id_s.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        money       = money.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        acctype     = acctype.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        interest    = interest.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        overdraft   = overdraft.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        old_primary = old_primary.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        open_date   = open_date.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        cashtype    = cashtype.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        bank        = bank.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        ownerid     = ownerid.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        overdraft   = overdraft.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')

        sqlcommand = ""
        if len(old_primary) > 0 : # 改 #
            if acctype == "0" :
                sqlcommand = sqlcommand + " UPDATE DEPOSIT_ACCOUNT SET   "
                if len(money) > 0 :
                    sqlcommand = sqlcommand + " DEPOSIT_ACCOUNT_MONEY = '"          + money     + "',"
                if len(interest) > 0 :
                    sqlcommand = sqlcommand + " DEPOSIT_ACCOUNT_INTERESTRATE = '"   + interest  + "',"
                
                sqlcommand = sqlcommand[:len(sqlcommand) - 1]
                sqlcommand = sqlcommand + " WHERE DEPOSIT_ACCOUNT_ID = '" + id_s + "'"
            else :
                sqlcommand = sqlcommand + " UPDATE CHECK_ACCOUNT SET   "
                if len(money) > 0 :
                    sqlcommand = sqlcommand + " CHECK_ACCOUNT_MONEY = '"        + money     + "',"
                if len(overdraft) > 0 :
                    sqlcommand = sqlcommand + " CHECK_ACCOUNT_OVERDRAFT = '"    + overdraft + "',"
                
                sqlcommand = sqlcommand[:len(sqlcommand) - 1]
                sqlcommand = sqlcommand + " WHERE CHECK_ACCOUNT_ID = '" + id_s + "'"
        else : # 增 #
            if acctype == "0" :
                insert = "("
                insert = insert + "'"           + id_s      + "'"               + ","
                insert = insert + "'"           + money     + "'"               + ","
                insert = insert + "TO_DATE('"   + open_date + "','YYYY-MM-DD')" + ","
                insert = insert + "'"           + interest  + "'"               + ","
                insert = insert + "'"           + cashtype  + "'"
                insert = insert + ")"
                sqlcommand =    sqlcommand + \
                                "   INSERT \
                                    INTO DEPOSIT_ACCOUNT(   DEPOSIT_ACCOUNT_ID,             \
                                                            DEPOSIT_ACCOUNT_MONEY,          \
                                                            DEPOSIT_ACCOUNT_REGDATE,        \
                                                            DEPOSIT_ACCOUNT_INTERESTRATE,   \
                                                            DEPOSIT_ACCOUNT_CURRENCYTYPE    \
                                                        )\
                                    VALUES \
                                " + insert

                print(sqlcommand)
                cursor.execute(sqlcommand)
                sqlcommand = ""

                insert = "("
                insert = insert + "'"           + bank      + "'"               + ","
                insert = insert + "'"           + ownerid   + "'"               + ","
                insert = insert + "'"           + id_s      + "'"               + ","
                insert = insert + "TO_DATE('"   + open_date + "','YYYY-MM-DD')"
                insert = insert + ")"
                sqlcommand =    sqlcommand + \
                                "   INSERT \
                                    INTO CUSTOMER_DEPOSIT_ACCOUNT(  BANK_NAME,\
                                                                    CUSTOMER_ID, \
                                                                    DEPOSIT_ACCOUNT_ID, \
                                                                    LAST_VIEW\
                                                                    )\
                                    VALUES \
                                " + insert
            else :
                insert = "("
                insert = insert + "'"           + id_s      + "'"               + ","
                insert = insert + "'"           + money     + "'"               + ","
                insert = insert + "TO_DATE('"   + open_date + "','YYYY-MM-DD')" + ","
                insert = insert + "'"           + overdraft  + "'"
                insert = insert + ")"
                sqlcommand =    sqlcommand + \
                                "   INSERT \
                                    INTO CHECK_ACCOUNT(     CHECK_ACCOUNT_ID,             \
                                                            CHECK_ACCOUNT_MONEY,          \
                                                            CHECK_ACCOUNT_REGDATE,        \
                                                            CHECK_ACCOUNT_OVERDRAFT         \
                                                        )\
                                    VALUES \
                                " + insert

                print(sqlcommand)
                cursor.execute(sqlcommand)
                sqlcommand = ""

                insert = "("
                insert = insert + "'"           + bank      + "'"               + ","
                insert = insert + "'"           + ownerid   + "'"               + ","
                insert = insert + "'"           + id_s      + "'"               + ","
                insert = insert + "TO_DATE('"   + open_date + "','YYYY-MM-DD')"
                insert = insert + ")"
                sqlcommand =    sqlcommand + \
                                "   INSERT \
                                    INTO CUSTOMER_CHECK_ACCOUNT(    BANK_NAME,\
                                                                    CUSTOMER_ID, \
                                                                    CHECK_ACCOUNT_ID, \
                                                                    LAST_VIEW\
                                                                    )\
                                    VALUES \
                                " + insert

        print(sqlcommand)
        try :
            cursor.execute(sqlcommand)
        except :
            cursor.close()
            connection.close()
            response = make_response(jsonify({    
                                            'code':400,
                                            'msg': 'fail'
                                            })
                                    )
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response

        cursor.close()
        connection.commit()
        connection.close()
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

        primary = request.form['primary']
        acctype = request.form['acctype']
        primary = primary.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        acctype = acctype.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')

        if acctype == "0" :
            sqlcommand = " SELECT * FROM DEPOSIT_ACCOUNT WHERE "
            sqlcommand = sqlcommand + " DEPOSIT_ACCOUNT_ID = '" + primary + "'"
            sqlcommand = sqlcommand + " AND DEPOSIT_ACCOUNT_MONEY > 0 "
            print(sqlcommand)
            cursor.execute(sqlcommand)
            # 使读取的 Oracle 数据字典化
            cursor.rowfactory = makeDictFactory(cursor)
            result = cursor.fetchall()
            if len(result) > 0 :
                cursor.close()
                connection.close()
                response = make_response(jsonify({    
                                                'code': 413,
                                                'msg': '尚有余额不能删除'
                                                })
                                        )
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
                response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
                return response

            sqlcommand = " DELETE FROM CUSTOMER_DEPOSIT_ACCOUNT WHERE "
            sqlcommand = sqlcommand + " DEPOSIT_ACCOUNT_ID = '" + primary + "'"
            print(sqlcommand)
            cursor.execute(sqlcommand)

            sqlcommand = " DELETE FROM DEPOSIT_ACCOUNT WHERE "
            sqlcommand = sqlcommand + " DEPOSIT_ACCOUNT_ID = '" + primary + "'"
            print(sqlcommand)
            cursor.execute(sqlcommand)

            cursor.close()
            connection.commit()
            connection.close()

        else :
            sqlcommand = " SELECT * FROM CHECK_ACCOUNT WHERE "
            sqlcommand = sqlcommand + " CHECK_ACCOUNT_ID = '" + primary + "'"
            sqlcommand = sqlcommand + " AND CHECK_ACCOUNT_MONEY > 0 "
            print(sqlcommand)
            cursor.execute(sqlcommand)
            # 使读取的 Oracle 数据字典化
            cursor.rowfactory = makeDictFactory(cursor)
            result = cursor.fetchall()
            if len(result) > 0 :
                cursor.close()
                connection.close()
                response = make_response(jsonify({    
                                                'code': 413,
                                                'msg': '尚有余额不能删除'
                                                })
                                        )
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
                response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
                return response

            sqlcommand = " DELETE FROM CUSTOMER_CHECK_ACCOUNT WHERE "
            sqlcommand = sqlcommand + " CHECK_ACCOUNT_ID = '" + primary + "'"
            print(sqlcommand)
            cursor.execute(sqlcommand)

            sqlcommand = " DELETE FROM CHECK_ACCOUNT WHERE "
            sqlcommand = sqlcommand + " CHECK_ACCOUNT_ID = '" + primary + "'"
            print(sqlcommand)
            cursor.execute(sqlcommand)

            cursor.close()
            connection.commit()
            connection.close()

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
@account_api.route('/accountCustomer',methods=['POST'])
def accountCustomer():   
    rstype=request.form['type']
    # id=request.form['accID'] # 账户号，用于查询和新增户主
    # bank=request.form['bank'] # 开户银行
    # ownerID=request.form['ownerID'] # 户主身份证号，用于新增记录
    print(rstype)
    if (rstype=="Search"):
        # Todo: 实现数据库操作，返回查询的结果
        print('Search')

        connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
        cursor = connection.cursor()

        accid   = request.form['accid']
        bank    = request.form['bank']
        acctype = request.form['acctype']
        accid   = accid.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        bank    = bank.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        acctype = acctype.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')

        sqlcommand = ""
        if acctype == "0" :
            sqlcommand = sqlcommand + " SELECT"
            sqlcommand = sqlcommand + " CUSTOMER_DEPOSIT_ACCOUNT.LAST_VIEW AS visit_date"   + ','
            sqlcommand = sqlcommand + " CUSTOMER.CUSTOMER_NAME AS ownername"                + ','
            sqlcommand = sqlcommand + " CUSTOMER_DEPOSIT_ACCOUNT.CUSTOMER_ID AS ownerid"
            sqlcommand = sqlcommand + " FROM"
            sqlcommand = sqlcommand + " CUSTOMER_DEPOSIT_ACCOUNT,"
            sqlcommand = sqlcommand + " CUSTOMER"
            sqlcommand = sqlcommand + " WHERE"
            sqlcommand = sqlcommand + " CUSTOMER.CUSTOMER_ID = CUSTOMER_DEPOSIT_ACCOUNT.CUSTOMER_ID"
            sqlcommand = sqlcommand + " AND CUSTOMER_DEPOSIT_ACCOUNT.BANK_NAME = '"             + bank  + "'"
            sqlcommand = sqlcommand + " AND CUSTOMER_DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_ID = '"    + accid + "'"
        else:
            sqlcommand = sqlcommand + " SELECT"
            sqlcommand = sqlcommand + " CUSTOMER_CHECK_ACCOUNT.LAST_VIEW AS visit_date"   + ','
            sqlcommand = sqlcommand + " CUSTOMER.CUSTOMER_NAME AS ownername"                + ','
            sqlcommand = sqlcommand + " CUSTOMER_CHECK_ACCOUNT.CUSTOMER_ID AS ownerid"
            sqlcommand = sqlcommand + " FROM"
            sqlcommand = sqlcommand + " CUSTOMER_CHECK_ACCOUNT,"
            sqlcommand = sqlcommand + " CUSTOMER"
            sqlcommand = sqlcommand + " WHERE"
            sqlcommand = sqlcommand + " CUSTOMER.CUSTOMER_ID = CUSTOMER_CHECK_ACCOUNT.CUSTOMER_ID"
            sqlcommand = sqlcommand + " AND CUSTOMER_CHECK_ACCOUNT.BANK_NAME = '"             + bank  + "'"
            sqlcommand = sqlcommand + " AND CUSTOMER_CHECK_ACCOUNT.CHECK_ACCOUNT_ID = '"    + accid + "'"
        
        print(sqlcommand)
        cursor.execute(sqlcommand)
        # 使读取的 Oracle 数据字典化
        cursor.rowfactory = makeDictFactory(cursor)
        result = cursor.fetchall()
        for line in result:
            line['visit_date']  = line['visit_date'].strftime('%Y-%m-%d')

        if result :
            response = make_response(jsonify({    
                                            'code': 200,
                                            'list': result
                                            # [
                                            #     {'ownerid':'11111','ownername':'柳树'},
                                            #     {'ownerid':'11112','ownername':'杨树'},
                                            #     {'ownerid':'11222','ownername':'柏树'}
                                            # ]
                                        })
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
        response.headers['Access-Control-Allow-Origin']  = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response

    if (rstype=="Insert"):
        # Todo: 实现数据库操作，新增记录
        print('Insert')

        connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
        cursor = connection.cursor()

        accid       = request.form['accid'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        # 账户号，用于查询和新增户主
        bank        = request.form['bank'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        # 开户银行
        ownerid     = request.form['ownerid'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        # 户主身份证号，用于新增记录
        visit_date  = request.form['visit_date'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        acctype     = request.form['acctype'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
            
        sqlcommand = ""

        if acctype == "0" :
            insert = "("
            insert = insert + "'"           + bank       + "'"               + ","
            insert = insert + "'"           + ownerid    + "'"               + ","
            insert = insert + "'"           + accid      + "'"               + ","
            insert = insert + "TO_DATE('"   + visit_date + "','YYYY-MM-DD')"
            insert = insert + ")"
            sqlcommand =    sqlcommand + \
                            "   INSERT \
                                INTO CUSTOMER_DEPOSIT_ACCOUNT(  BANK_NAME,\
                                                                CUSTOMER_ID, \
                                                                DEPOSIT_ACCOUNT_ID, \
                                                                LAST_VIEW\
                                                                )\
                                VALUES \
                            " + insert
        else :
            insert = "("
            insert = insert + "'"           + bank       + "'"               + ","
            insert = insert + "'"           + ownerid    + "'"               + ","
            insert = insert + "'"           + accid      + "'"               + ","
            insert = insert + "TO_DATE('"   + visit_date + "','YYYY-MM-DD')"
            insert = insert + ")"
            sqlcommand =    sqlcommand + \
                            "   INSERT \
                                INTO CUSTOMER_CHECK_ACCOUNT(    BANK_NAME,\
                                                                CUSTOMER_ID, \
                                                                CHECK_ACCOUNT_ID, \
                                                                LAST_VIEW\
                                                                )\
                                VALUES \
                            " + insert
        
        print(sqlcommand)
        try :
            cursor.execute(sqlcommand)
        except :
            cursor.close()
            connection.close()
            response = make_response(jsonify({    
                                            'code':400,
                                            'msg': 'fail'
                                            })
                                    )
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response

        sqlcommand = " SELECT"
        sqlcommand = sqlcommand + " CUSTOMER_NAME AS ownername "
        sqlcommand = sqlcommand + " FROM"
        sqlcommand = sqlcommand + " CUSTOMER"
        sqlcommand = sqlcommand + " WHERE"
        sqlcommand = sqlcommand + " CUSTOMER_ID = '" + ownerid + "'"

        print(sqlcommand)
        cursor.execute(sqlcommand)
        # 使读取的 Oracle 数据字典化
        cursor.rowfactory = makeDictFactory(cursor)
        result = cursor.fetchone()
        result['id']      = accid
        result['bank']    = bank
        result['ownerid'] = ownerid

        cursor.close()
        connection.commit()
        connection.close()
        response = make_response(jsonify({    
                                        'code':200,
                                        'record': result
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

        accid   = request.form['accid'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        bank    = request.form['bank'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        ownerid = request.form['ownerid'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        acctype = request.form['acctype'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        
        if acctype == "0" :
            sqlcommand = " DELETE FROM CUSTOMER_DEPOSIT_ACCOUNT WHERE "
            sqlcommand = sqlcommand + " DEPOSIT_ACCOUNT_ID  = '" + accid     + "'"
            sqlcommand = sqlcommand + " AND CUSTOMER_ID     = '" + ownerid   + "'"
            sqlcommand = sqlcommand + " AND BANK_NAME       = '" + bank      + "'"
            print(sqlcommand)
            cursor.execute(sqlcommand)
        else :
            sqlcommand = " DELETE FROM CUSTOMER_CHECK_ACCOUNT WHERE "
            sqlcommand = sqlcommand + " CHECK_ACCOUNT_ID  = '" + accid     + "'"
            sqlcommand = sqlcommand + " AND CUSTOMER_ID     = '" + ownerid   + "'"
            sqlcommand = sqlcommand + " AND BANK_NAME       = '" + bank      + "'"
            print(sqlcommand)
            cursor.execute(sqlcommand)

        cursor.close()
        connection.commit()
        connection.close()

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