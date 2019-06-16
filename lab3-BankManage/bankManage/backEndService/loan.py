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

        connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
        cursor = connection.cursor()

        idSearch     = request.form['idSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        bankSearch   = request.form['bankSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        statusSearch = request.form['statusSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        custSearch   = request.form['custSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        upperBound   = request.form['upperBound'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        lowerBound   = request.form['lowerBound'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  

        sqlcommand = ""
        sqlcommand = sqlcommand + " SELECT"
        sqlcommand = sqlcommand + " LOAN.LOAN_ID            AS id"          + ','
        sqlcommand = sqlcommand + " CUSTOMER.CUSTOMER_NAME  AS customer"    + ','
        sqlcommand = sqlcommand + " LOAN.LOAN_MONEY         AS amount"      + ','
        sqlcommand = sqlcommand + " LOAN.STATUS             AS status"      + ','
        sqlcommand = sqlcommand + " LOAN.BANK_NAME          AS bank"
        sqlcommand = sqlcommand + " FROM"
        sqlcommand = sqlcommand + " LOAN, CUSTOMER, LOAN_CUSTOMER"
        sqlcommand = sqlcommand + " WHERE"
        sqlcommand = sqlcommand + " LOAN_CUSTOMER.CUSTOMER_ID = CUSTOMER.CUSTOMER_ID "
        sqlcommand = sqlcommand + " AND LOAN_CUSTOMER.LOAN_ID = LOAN.LOAN_ID" 
        if (len(lowerBound) > 0) :
            sqlcommand = sqlcommand + " AND LOAN.STATUS             = "         + statusSearch
        if (len(lowerBound) > 0) :
            sqlcommand = sqlcommand + " AND LOAN.LOAN_ID            LIKE '%"    + idSearch      + "%'"
        if (len(lowerBound) > 0) :
            sqlcommand = sqlcommand + " AND LOAN.BANK_NAME          LIKE '%"    + bankSearch    + "%'"
        if (len(lowerBound) > 0) :
            sqlcommand = sqlcommand + " AND CUSTOMER.CUSTOMER_NAME  LIKE '%"    + custSearch    + "%'"
        if (len(upperBound) > 0) :
            sqlcommand = sqlcommand + " AND LOAN.LOAN_MONEY < " + upperBound
        if (len(lowerBound) > 0) :
            sqlcommand = sqlcommand + " AND LOAN.LOAN_MONEY > " + lowerBound

        print(sqlcommand)
        cursor.execute(sqlcommand)
        # 使读取的 Oracle 数据字典化
        cursor.rowfactory = makeDictFactory(cursor)
        result = cursor.fetchall()
        for line in result:
            line['id']      = str(line['id'])

        if result :
            response = make_response(jsonify({    
                                            'code':200,
                                            'list': result
                                            # [
                                            #     {'id': "123000",'customer': "张三",'bank': "合肥支行",'amount':2563.00,'status':'1'},
                                            #     {'id': "123001",'customer': "李四",'bank': "合肥支行",'amount':252263.00,'status':'0'},
                                            #     {'id': "123023",'customer': "王五",'bank': "合肥支行",'amount':25.00,'status':'2'}
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

    if (rstype=="Update"):
        # Todo: 实现数据库操作，修改或新增记录
        print('Update')

        connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
        cursor = connection.cursor()

        id_s        = request.form['id'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        bank        = request.form['bank'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        customer    = request.form['customer'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        amount      = request.form['amount'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        status      = request.form['status'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        old_primary = request.form['old_primary'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  

        sqlcommand = ""
        insert = "("
        insert = insert + "'" + id_s    + "'" + ","
        insert = insert + "'" + bank    + "'" + ","
        insert = insert       + amount        + ","
        insert = insert       + status  
        insert = insert + ")"
        sqlcommand =    sqlcommand + \
                        "   INSERT \
                            INTO LOAN(  LOAN_ID,        \
                                        BANK_NAME,      \
                                        LOAN_MONEY,     \
                                        STATUS          \
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

        sqlcommand = ""
        insert = "("
        insert = insert + "'" + customer + "'" + ","
        insert = insert + "'" + id_s     + "'"
        insert = insert + ")"
        sqlcommand =    sqlcommand +                                    \
                        "   INSERT                                      \
                            INTO LOAN_CUSTOMER (CUSTOMER_ID,LOAN_ID)    \
                            VALUES                                      \
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

        primary = request.form['primary'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        
        sqlcommand = ""
        sqlcommand = sqlcommand + " SELECT * "
        sqlcommand = sqlcommand + " FROM"
        sqlcommand = sqlcommand + " LOAN"
        sqlcommand = sqlcommand + " WHERE"
        sqlcommand = sqlcommand + "     LOAN.LOAN_ID = '" + primary + "'"
        sqlcommand = sqlcommand + " AND LOAN.STATUS = 1"

        print(sqlcommand)
        cursor.execute(sqlcommand)
        # 使读取的 Oracle 数据字典化
        cursor.rowfactory = makeDictFactory(cursor)
        result = cursor.fetchall()
        if len(result) > 0 :
            cursor.close()
            connection.close()
            response = make_response(jsonify({    
                                            'code': 417,
                                            'msg': '贷款正在发放，无法删除'
                                            })
                                    )
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response

        sqlcommand = "ALTER TABLE LOAN_CUSTOMER DROP CONSTRAINT FK_LC_LOAN_ID"
        cursor.execute(sqlcommand)
        sqlcommand = "ALTER TABLE LOAN_CUSTOMER DROP CONSTRAINT FK_LC_CUSTOMER_ID"
        cursor.execute(sqlcommand)

        sqlcommand = " DELETE FROM LOAN_CUSTOMER WHERE "
        sqlcommand = sqlcommand + " LOAN_ID = '" + primary + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)

        sqlcommand = "ALTER TABLE LOAN_CUSTOMER ADD CONSTRAINT FK_LC_LOAN_ID        FOREIGN KEY(LOAN_ID)        REFERENCES LOAN(LOAN_ID)"
        cursor.execute(sqlcommand)
        sqlcommand = "ALTER TABLE LOAN_CUSTOMER ADD CONSTRAINT FK_LC_CUSTOMER_ID    FOREIGN KEY(CUSTOMER_ID)    REFERENCES CUSTOMER(CUSTOMER_ID)"
        cursor.execute(sqlcommand)

        sqlcommand = " DELETE FROM PAY WHERE "
        sqlcommand = sqlcommand + " LOAN_ID = '" + primary + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)

        sqlcommand = " DELETE FROM LOAN WHERE "
        sqlcommand = sqlcommand + " LOAN_ID = '" + primary + "'"
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
@loan_api.route('/pay',methods=['POST'])
def pay():
    rstype=request.form['type']
    # id=request.form['loanID'] # 贷款号，用于查询和新增支付记录
    # date=request.form['date'] # 支付日期，用于新增记录
    # money=request.form['money'] # 支付金额，用于新增记录

    if (rstype=="Search"):
        # Todo: 实现数据库操作，返回查询的结果
        print('Search')

        connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
        cursor = connection.cursor()

        loanid = request.form['loanid'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  

        sqlcommand = ""
        sqlcommand = sqlcommand + " SELECT "
        sqlcommand = sqlcommand + " PAY_DATE AS date_s"   + ','
        sqlcommand = sqlcommand + " PAY_MONEY AS money"
        sqlcommand = sqlcommand + " FROM"
        sqlcommand = sqlcommand + " PAY"
        sqlcommand = sqlcommand + " WHERE"
        sqlcommand = sqlcommand + " LOAN_ID = '" + loanid + "'"

        print(sqlcommand)
        cursor.execute(sqlcommand)
        # 使读取的 Oracle 数据字典化
        cursor.rowfactory = makeDictFactory(cursor)
        result = cursor.fetchall()
        for line in result:
            line['date_s']  = line['date_s'].strftime('%Y-%m-%d')

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
                    'code': 400,
                    'list': []
                }
            )
        )
        response.headers['Access-Control-Allow-Origin']  = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response

    if (rstype=="Insert"):
        # Todo: 实现数据库操作，修改或新增记录
        print('Insert')

        connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
        cursor = connection.cursor()

        loanid = request.form['loanid'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        date   = request.form['date'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        money  = request.form['money'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  

        sqlcommand = ""
        sqlcommand = sqlcommand + " SELECT "
        sqlcommand = sqlcommand + " STATUS AS status"       + ','
        sqlcommand = sqlcommand + " LOAN_MONEY AS money"
        sqlcommand = sqlcommand + " FROM"
        sqlcommand = sqlcommand + " LOAN"
        sqlcommand = sqlcommand + " WHERE"
        sqlcommand = sqlcommand + " LOAN_ID = '" + loanid + "'"

        print(sqlcommand)
        cursor.execute(sqlcommand)
        # 使读取的 Oracle 数据字典化
        cursor.rowfactory = makeDictFactory(cursor)
        result = cursor.fetchone()

        if result :
            loanlimit = result['money']
            if result['status'] == 2:
                response = make_response(
                    jsonify(
                        {
                            'code': 422,
                            'msg': '贷款已全部发放'
                        }
                    )
                )
                response.headers['Access-Control-Allow-Origin']  = '*'
                response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
                response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
                return response
            else :
                sqlcommand = ""
                sqlcommand = sqlcommand + " SELECT "
                sqlcommand = sqlcommand + " LOAN_ID, SUM(PAY_MONEY) AS alreadypay"
                sqlcommand = sqlcommand + " FROM"
                sqlcommand = sqlcommand + " ("
                sqlcommand = sqlcommand + "     SELECT * FROM PAY WHERE LOAN_ID = '" + loanid + "'"
                sqlcommand = sqlcommand + " )PAY_THIS"
                sqlcommand = sqlcommand + " GROUP BY LOAN_ID"
                # sqlcommand = sqlcommand + " LOAN_ID = '" + loanid + "'"

                print(sqlcommand)
                cursor.execute(sqlcommand)
                # 使读取的 Oracle 数据字典化
                cursor.rowfactory = makeDictFactory(cursor)
                result = cursor.fetchone()
                print(result)
                alreadypay = 0
                if result :
                    alreadypay = result['alreadypay']

                print(loanlimit)
                print(alreadypay)
                print(money)

                loanlimit  = float(loanlimit)
                alreadypay = float(alreadypay)
                money      = float(money)

                if loanlimit < alreadypay + money:
                    response = make_response(
                        jsonify(
                            {
                                'code': 423,
                                'msg': '超过贷款额度'
                            }
                        )
                    )
                    response.headers['Access-Control-Allow-Origin']  = '*'
                    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
                    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
                    return response

                if loanlimit == alreadypay + money :
                    sqlcommand = " UPDATE LOAN SET STATUS = 2 WHERE LOAN_ID = \'" + loanid + "'"
                    print(sqlcommand)
                    cursor.execute(sqlcommand)
                else :
                    sqlcommand = " UPDATE LOAN SET STATUS = 1 WHERE LOAN_ID = \'" + loanid + "'"
                    print(sqlcommand)
                    cursor.execute(sqlcommand)

                sqlcommand = ""
                insert = "("
                insert = insert + "'"           + loanid    + "'"               + ","
                insert = insert + "TO_DATE('"   + date      + "','YYYY-MM-DD')" + ","
                insert = insert                 + str(money)   
                insert = insert + ")"
                sqlcommand =    sqlcommand +                                    \
                                "   INSERT                                      \
                                    INTO PAY (LOAN_ID,PAY_DATE,PAY_MONEY)       \
                                    VALUES                                      \
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
#==============================================================================================
# Oracle 数据字典化函数
def makeDictFactory(cursor):
    columnNames = [d[0].lower() for d in cursor.description]
    def createRow(*args):
        return dict(zip(columnNames, args))
    return createRow
