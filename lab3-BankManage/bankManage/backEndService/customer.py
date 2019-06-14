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
            sqlcommand = sqlcommand + " AND CUSTOMER_NAME LIKE '%"      + nameSearch + "%'"
        if (len(idSearch) > 0) :
            sqlcommand = sqlcommand + " AND CUSTOMER_ID LIKE '%"        + idSearch + "%'"
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
        connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
        cursor = connection.cursor()
        # print(request.form)
        id_s        = request.form['id']
        name        = request.form['name']
        name        = name.rstrip()
        tel         = request.form['tel']
        tel         = tel.rstrip()
        addr        = request.form['addr']
        addr        = addr.rstrip()
        name_link   = request.form['name_link']
        name_link   = name_link.rstrip()
        tel_link    = request.form['tel_link']
        tel_link    = tel_link.rstrip()
        email_link  = request.form['email_link']
        email_link  = email_link.rstrip()
        relation    = request.form['relation']
        relation    = relation.rstrip()
        old_primary = request.form['old_primary']
        old_primary = old_primary.rstrip()
        print("hello")

        sqlcommand = ""
        if len(old_primary) > 0 : # 改 #
            if id_s != old_primary :
                result = cursor.var(cx_Oracle.NUMBER)
                cursor.callproc('CHANGE_CUSTOMER_NAME',[old_primary, id_s, result ])
                print(result)
                if result.getvalue() == 2 :
                    cursor.close()
                    connection.close()
                    response = make_response(jsonify({    
                                                        'code':402,
                                                        'msg': 'old name do not find'
                                                    })
                                            )
                    response.headers['Access-Control-Allow-Origin']  = '*'
                    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
                    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
                    return response
                if result.getvalue() == 1 :
                    cursor.close()
                    connection.close()
                    response = make_response(jsonify({    
                                                        'code':401,
                                                        'msg': 'new name used'
                                                    })
                                            )
                    response.headers['Access-Control-Allow-Origin']  = '*'
                    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
                    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
                    return response
            
            sqlcommand = sqlcommand + " UPDATE CUSTOMER SET   "
            if len(name) > 0 :
                sqlcommand = sqlcommand + " CUSTOMER_NAME = '"              + name + "',"
            if len(tel) > 0 :
                sqlcommand = sqlcommand + " CUSTOMER_PHONE = '"             + tel + "',"
            if len(addr) > 0 :
                sqlcommand = sqlcommand + " CUSTOMER_ADDRESS = '"           + addr + "',"
            if len(name_link) > 0 :
                sqlcommand = sqlcommand + " CUSTOMER_CONTACT_NAME = '"      + name_link + "',"
            if len(tel_link) > 0 :
                sqlcommand = sqlcommand + " CUSTOMER_CONTACT_PHONE = '"     + tel_link + "',"
            if len(email_link) > 0 :
                sqlcommand = sqlcommand + " CUSTOMER_CONTACT_EMAIL = '"     + email_link + "',"
            if len(relation) > 0 :
                sqlcommand = sqlcommand + " CUSTOMER_CONTACT_RELATION = '"  + relation + "',"


            sqlcommand = sqlcommand[:len(sqlcommand) - 1]
            sqlcommand = sqlcommand + " WHERE CUSTOMER_ID = '" + id_s + "'"
            
        else : # 增 #
            insert = "("
            insert = insert + "'" + id_s        + "'" + ","
            insert = insert + "'" + name        + "'" + ","
            insert = insert + "'" + tel         + "'" + ","
            insert = insert + "'" + addr        + "'" + ","
            insert = insert + "'" + name_link   + "'" + ","
            insert = insert + "'" + tel_link    + "'" + ","
            insert = insert + "'" + email_link  + "'" + ","
            insert = insert + "'" + relation    + "'" 
            insert = insert + ")"
            sqlcommand =    sqlcommand + \
                            "   INSERT \
                                INTO CUSTOMER(  CUSTOMER_ID,        CUSTOMER_NAME, CUSTOMER_PHONE,\
                                                CUSTOMER_ADDRESS,   CUSTOMER_CONTACT_NAME,\
                                                CUSTOMER_CONTACT_PHONE,\
                                                CUSTOMER_CONTACT_EMAIL,\
                                                CUSTOMER_CONTACT_RELATION\
                                                ) \
                                VALUES \
                            " \
                            + insert
        
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
        primary = primary.rstrip()
    #==============================================================================
        sqlcommand = " SELECT * FROM EMPLOYEE_CUSTOMER WHERE "
        sqlcommand = sqlcommand + " CUSTOMER_ID = '" + primary + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        # 使读取的 Oracle 数据字典化
        cursor.rowfactory = makeDictFactory(cursor)
        result = cursor.fetchall()
        if len(result) > 0 :
            cursor.close()
            connection.close()
            response = make_response(jsonify({    
                                            'code': 407,
                                            'msg': '有关联员工信息'
                                            })
                                    )
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response
    #==============================================================================
        sqlcommand = " SELECT * FROM CUSTOMER_DEPOSIT_ACCOUNT WHERE "
        sqlcommand = sqlcommand + " CUSTOMER_ID = '" + primary + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        # 使读取的 Oracle 数据字典化
        cursor.rowfactory = makeDictFactory(cursor)
        result = cursor.fetchall()
        if len(result) > 0 :
            cursor.close()
            connection.close()
            response = make_response(jsonify({    
                                            'code': 408,
                                            'msg': '有关联存储账户信息'
                                            })
                                    )
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response
    #==============================================================================
        sqlcommand = " SELECT * FROM CUSTOMER_CHECK_ACCOUNT WHERE "
        sqlcommand = sqlcommand + " CUSTOMER_ID = '" + primary + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        # 使读取的 Oracle 数据字典化
        cursor.rowfactory = makeDictFactory(cursor)
        result = cursor.fetchall()
        if len(result) > 0 :
            cursor.close()
            connection.close()
            response = make_response(jsonify({    
                                            'code': 409,
                                            'msg': '有关联支票账户信息'
                                            })
                                    )
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response
    #==============================================================================
        sqlcommand = " SELECT * FROM LOAN_CUSTOMER WHERE "
        sqlcommand = sqlcommand + " CUSTOMER_ID = '" + primary + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        # 使读取的 Oracle 数据字典化
        cursor.rowfactory = makeDictFactory(cursor)
        result = cursor.fetchall()
        if len(result) > 0 :
            cursor.close()
            connection.close()
            response = make_response(jsonify({    
                                            'code': 410,
                                            'msg': '有关联贷款信息'
                                            })
                                    )
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response
    #==============================================================================
        sqlcommand = " DELETE FROM CUSTOMER WHERE "
        sqlcommand = sqlcommand + " CUSTOMER_ID = '" + primary + "'"
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