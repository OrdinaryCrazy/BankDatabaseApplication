from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from flask_cors import *
import json
import time
import cx_Oracle
from datetime import datetime

from flask import Blueprint

staff_api = Blueprint('staff_api', __name__)

#==============================================================================================
# 员工管理 后台功能
@staff_api.route('/staff',methods=['POST'])
def staff():
    rstype=request.form['type']
    print(request.form)
    if (rstype=="Search"):
        print('Search') # 查 #
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
            sqlcommand = sqlcommand + " AND EMPLOYEE_ADDRESS LIKE '%" + addrSearch + "%'"
        if (len(lowerBound) > 0) :
            sqlcommand = sqlcommand + " AND EMPLOYEE_ENTERDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
        if (len(upperBound) > 0) :
            sqlcommand = sqlcommand + " AND EMPLOYEE_ENTERDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"

        print(sqlcommand)
        cursor.execute(sqlcommand)
        # 使读取的 Oracle 数据字典化
        cursor.rowfactory = makeDictFactory(cursor)
        result = cursor.fetchall()
        # print(result)
        for line in result:
            line['id']      = str(line['id'])
            line['date_s']  = line['date_s'].strftime('%Y-%m-%d')
        # print(result)

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
        print('Update')
        # Todo: 实现数据库操作，修改或新增记录
        connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
        cursor = connection.cursor()
        # print(request.form)
        id_s        = request.form['id']
        name        = request.form['name']
        name        = name.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        bank        = request.form['bank']
        bank        = bank.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        dept        = request.form['dept']
        tel         = request.form['tel']
        addr        = request.form['addr']
        addr        = addr.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        date_s      = request.form['date_s']
        old_primary = request.form['old_primary']
        old_primary = old_primary.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        print("hello")

        sqlcommand = ""
        if len(old_primary) > 0 : # 改 #
            if id_s != old_primary :
                result = cursor.var(cx_Oracle.NUMBER)
                cursor.callproc('CHANGE_EMPLOYEE_NAME',[old_primary, id_s, result ])
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
            
            sqlcommand = sqlcommand + " UPDATE EMPLOYEE SET   "
            if len(name) > 0 :
                sqlcommand = sqlcommand + " EMPLOYEE_NAME = '" + name + "',"
            if len(bank) > 0 :
                sqlcommand = sqlcommand + " EMPLOYEE_BANK_NAME = '" + bank + "',"
            if len(dept) > 0 :
                sqlcommand = sqlcommand + " EMPLOYEE_DEPART_ID = '" + dept + "',"
            if len(tel) > 0 :
                sqlcommand = sqlcommand + " EMPLOYEE_PHONE = '" + tel + "',"
            if len(addr) > 0 :
                sqlcommand = sqlcommand + " EMPLOYEE_ADDRESS = '" + addr + "',"
            if len(date_s) > 0 :
                sqlcommand = sqlcommand + " EMPLOYEE_ENTERDATE = TO_DATE('" + date_s + "','YYYY-MM-DD'),"

            sqlcommand = sqlcommand[:len(sqlcommand) - 1]
            sqlcommand = sqlcommand + " WHERE EMPLOYEE_ID = '" + id_s + "'"
            
        else : # 增 #
            insert = "("
            insert = insert + "'" + id_s    + "'" + ","
            insert = insert + "'" + name    + "'" + ","
            insert = insert + "'" + bank    + "'" + ","
            insert = insert + "'" + dept    + "'" + ","
            insert = insert + "'" + tel     + "'" + ","
            insert = insert + "'" + addr    + "'" + ","
            insert = insert + "TO_DATE('" + date_s + "','YYYY-MM-DD')"
            insert = insert + ")"
            sqlcommand =    sqlcommand + \
                            "   INSERT \
                                INTO EMPLOYEE(  EMPLOYEE_ID,        EMPLOYEE_NAME, EMPLOYEE_BANK_NAME,\
                                                EMPLOYEE_DEPART_ID, EMPLOYEE_PHONE,EMPLOYEE_ADDRESS,\
                                                EMPLOYEE_ENTERDATE\
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
        primary = primary.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')

        sqlcommand = " SELECT * FROM EMPLOYEE_CUSTOMER WHERE "
        sqlcommand = sqlcommand + " EMPLOYEE_ID = '" + primary + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        # 使读取的 Oracle 数据字典化
        cursor.rowfactory = makeDictFactory(cursor)
        result = cursor.fetchall()
        if len(result) > 0 :
            cursor.close()
            connection.close()
            response = make_response(jsonify({    
                                            'code': 403,
                                            'msg': '有关联客户信息'
                                            })
                                    )
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response
        
        sqlcommand = " DELETE FROM EMPLOYEE WHERE "
        sqlcommand = sqlcommand + " EMPLOYEE_ID = '" + primary + "'"
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
# 员工客户关系查询 后台功能
@staff_api.route('/staffCustomer',methods=['POST'])
def staffCustomer():
    rstype=request.form['type']
    if (rstype=="SearchByStaff"):
        # Todo: 实现数据库操作，返回查询的结果
        print('SearchByStaff')

        connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
        cursor = connection.cursor()

        staffID = request.form['staffID']
        staffID = staffID.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')

        sqlcommand = ""
        sqlcommand = sqlcommand + " SELECT"
        sqlcommand = sqlcommand + " EMPLOYEE_CUSTOMER.CUSTOMER_ID AS ID"    + ','
        sqlcommand = sqlcommand + " CUSTOMER.CUSTOMER_NAME AS name"      + ','
        sqlcommand = sqlcommand + " EMPLOYEE_CUSTOMER.SERVICETYPE AS type"
        sqlcommand = sqlcommand + " FROM"
        sqlcommand = sqlcommand + " EMPLOYEE_CUSTOMER, CUSTOMER"
        sqlcommand = sqlcommand + " WHERE"
        sqlcommand = sqlcommand + " EMPLOYEE_CUSTOMER.CUSTOMER_ID = CUSTOMER.CUSTOMER_ID AND"
        sqlcommand = sqlcommand + " EMPLOYEE_CUSTOMER.EMPLOYEE_ID = '" + staffID + "'"

        print(sqlcommand)
        cursor.execute(sqlcommand)
        # 使读取的 Oracle 数据字典化
        cursor.rowfactory = makeDictFactory(cursor)
        result = cursor.fetchall()
        # print(result)
        for line in result:
            line['id']      = str(line['id'])
        # print(result)

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

    if (rstype=='SearchByCustomer'):
        # Todo: 实现数据库操作，返回查询的结果
        custID = request.form['custid'] # 客户身份证号，查找所有关于该客户的员工联系
        custID = custID.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        print('SearchByCustomer')
        print(custID)

        connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
        cursor = connection.cursor()

        sqlcommand = ""
        sqlcommand = sqlcommand + " SELECT"
        sqlcommand = sqlcommand + " EMPLOYEE_CUSTOMER.EMPLOYEE_ID AS staffid"    + ','
        sqlcommand = sqlcommand + " EMPLOYEE.EMPLOYEE_NAME AS staffname"      + ','
        sqlcommand = sqlcommand + " EMPLOYEE_CUSTOMER.SERVICETYPE AS type"
        sqlcommand = sqlcommand + " FROM"
        sqlcommand = sqlcommand + " EMPLOYEE_CUSTOMER, EMPLOYEE"
        sqlcommand = sqlcommand + " WHERE"
        sqlcommand = sqlcommand + " EMPLOYEE_CUSTOMER.EMPLOYEE_ID = EMPLOYEE.EMPLOYEE_ID AND"
        sqlcommand = sqlcommand + " EMPLOYEE_CUSTOMER.CUSTOMER_ID = '" + custID + "'"

        print(sqlcommand)
        cursor.execute(sqlcommand)
        # 使读取的 Oracle 数据字典化
        cursor.rowfactory = makeDictFactory(cursor)
        result = cursor.fetchall()
        # print(result)
        for line in result:
            line['staffid'] = str(line['staffid'])
        # print(result)

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

        custID      = request.form['custID']
        custID      = custID.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        staffID     = request.form['staffID']
        staffID     = staffID.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        serviceType = request.form['serviceType']
        serviceType = serviceType.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        old_custID  = request.form['old_custID']
        old_custID  = old_custID.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        old_staffID = request.form['old_staffID']
        old_staffID = old_staffID.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')

        sqlcommand = ""
        # if      len(old_custID)  > 0 and len(old_staffID) == 0  \
        #     or  len(old_staffID) > 0 and len(old_custID)  == 0 : # 改 #
        if len(old_custID) > 0 and len(old_staffID) > 0 :
            sqlcommand = sqlcommand + " UPDATE EMPLOYEE_CUSTOMER SET   "
            if len(custID) > 0 :
                sqlcommand = sqlcommand + " CUSTOMER_ID = '" + custID + "',"
            if len(staffID) > 0 :
                sqlcommand = sqlcommand + " EMPLOYEE_ID = '" + staffID + "',"
            if len(serviceType) > 0 :
                sqlcommand = sqlcommand + " SERVICETYPE = '" + serviceType + "',"

            sqlcommand = sqlcommand[:len(sqlcommand) - 1]
            sqlcommand = sqlcommand + " WHERE CUSTOMER_ID = '" + old_custID + "'"
            sqlcommand = sqlcommand + " AND EMPLOYEE_ID = '" + old_staffID + "'"
            
        else : # 增 #
            insert = "("
            insert = insert + "'" + custID      + "'" + ","
            insert = insert + "'" + staffID     + "'" + ","
            insert = insert + "'" + serviceType + "'"
            insert = insert + ")"
            sqlcommand =    sqlcommand + \
                            "   INSERT \
                                INTO EMPLOYEE_CUSTOMER(CUSTOMER_ID, EMPLOYEE_ID, SERVICETYPE) \
                                VALUES " + insert
        
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

        custID = request.form['custID']
        custID = custID.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        staffID = request.form['staffID']
        staffID = staffID.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')

        
        sqlcommand = " DELETE FROM EMPLOYEE_CUSTOMER WHERE "
        sqlcommand = sqlcommand + " EMPLOYEE_ID = '" + staffID + "'"
        sqlcommand = sqlcommand + " AND CUSTOMER_ID = '" + custID + "'"
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