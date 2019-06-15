from flask                  import Flask
from flask                  import request
from flask                  import jsonify
from flask                  import make_response
from flask_cors             import *
import json
import time
import cx_Oracle
#==============================================================================================
# Oracle 数据字典化函数
def makeDictFactory(cursor):
    columnNames = [d[0].lower() for d in cursor.description]
    def createRow(*args):
        return dict(zip(columnNames, args))
    return createRow
#=====================================================================================================
# from sqlalchemy                 import Column, Integer, String, create_engine
# from sqlalchemy.orm             import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base		

# Base = declarative_base()

# class Post(Base):
# 	__tablename__ = 'SUB_BANK'
# 	BANK_NAME   = Column('BANK_NAME', Integer, primary_key=True)
# 	date   = Column('date', String)
# 	post   = Column('post', String)
# 	name   = Column('name', String)
# 	value  = Column('value', String)
# 	time   = Column('time', String)

# engine = create_engine('System/db2019@localhost/ORCL', echo=True)
# Database= sessionmaker(bind=engine)
#=====================================================================================================
from flask import Blueprint

bank_api = Blueprint('bank_api', __name__)

#==============================================================================================
# 支行管理 后台功能
@bank_api.route('/bank',methods=['POST'])
def bank():
    rstype=request.form['type']
#==============================================================================================
    if (rstype=="Search"):  # 查 #
        # Todo: 实现数据库操作，返回查询的结果
        connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
        cursor = connection.cursor()

        bankSearch = request.form['bankSearch']
        citySearch = request.form['citySearch']
        lowerBound = request.form['lowerBound']
        upperBound = request.form['upperBound']

        sqlcommand = ""
        sqlcommand = sqlcommand + " SELECT"
        sqlcommand = sqlcommand + " BANK_NAME AS name"      + ','
        sqlcommand = sqlcommand + " CITY AS city "          + ','
        sqlcommand = sqlcommand + " POSSESSION AS money"
        sqlcommand = sqlcommand + " FROM"
        sqlcommand = sqlcommand + " SUB_BANK"
        sqlcommand = sqlcommand + " WHERE"
        sqlcommand = sqlcommand + " BANK_NAME IS NOT NULL"
        if (len(bankSearch) > 0) :
            sqlcommand = sqlcommand + " AND BANK_NAME LIKE '%" + bankSearch + "%'"
        if (len(citySearch) > 0) :
            sqlcommand = sqlcommand + " AND CITY LIKE '%" + citySearch + "%'"
        if (len(lowerBound) > 0) :
            sqlcommand = sqlcommand + " AND POSSESSION >" + lowerBound
        if (len(upperBound) > 0) :
            sqlcommand = sqlcommand + " AND POSSESSION <" + upperBound
 
        print(sqlcommand)
        cursor.execute(sqlcommand)
        # 使读取的 Oracle 数据字典化
        cursor.rowfactory = makeDictFactory(cursor)
        result = cursor.fetchall()

        # db = Database()
	    # query = db.query(Post).filter(Post.name.like('%xxx'))
	    # print query.count()
	    # query = query.all()[30:40]
	    # for x in query:
		#     print x.id, x.name
        # response = make_response(jsonify({    
        #                                 'code':200,
        #                                 'list':[
        #                                     {'name': '合肥城南支行','city': '合肥','money': 100000000},
        #                                     {'name': '南京城北支行','city': '南京','money': 102500000},
        #                                     {'name': '无锡城北支行','city': '无锡','money': 1000}
        #                                 ]
        #                             })
        #                         )
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
#==============================================================================================
    if (rstype=="Update"):
        # Todo: 实现数据库操作，修改或新增记录
        connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
        cursor = connection.cursor()

        name        = request.form['name']
        name        = name.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        city        = request.form['city']
        city        = city.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        money       = request.form['money']
        old_primary = request.form['old_primary']
        old_primary = old_primary.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')

        sqlcommand = ""
        if len(old_primary) > 0 : # 改 #
            if name != old_primary :
                # changeNameSQL = "CHANGE_BANK_NAME("
                # changeNameSQL = changeNameSQL + "'" + old_primary   + "'" + ","
                # changeNameSQL = changeNameSQL + "'" + name          + "'"
                # changeNameSQL = changeNameSQL + ");"
                # cursor.execute(changeNameSQL)
                result = cursor.var(cx_Oracle.NUMBER)
                # debugold = cursor.var(cx_Oracle.FIXED_CHAR)
                # debugnew = cursor.var(cx_Oracle.FIXED_CHAR)
                cursor.callproc('CHANGE_BANK_NAME',[old_primary, name, result ])
                # cursor.callproc('CHANGE_BANK_NAME',[ ("'" + old_primary + "'"), ("'" + name + "'"), result ])
                print(result.getvalue())
                print("'" + old_primary + "'")
                print("'" + name + "'")
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

            sqlcommand = sqlcommand + " UPDATE SUB_BANK SET   "
            if len(city) > 0 :
                sqlcommand = sqlcommand + " CITY = '" + city + "',"
            if len(money) > 0 :
                sqlcommand = sqlcommand + " POSSESSION = '" + money + "',"
            sqlcommand = sqlcommand[:len(sqlcommand) - 1]
            sqlcommand = sqlcommand + " WHERE BANK_NAME = '" + name + "'"
            
        else : # 增 #
            insert = "("
            insert = insert + "'" + name  + "'" + ","
            insert = insert + "'" + city  + "'" + ","
            insert = insert + "'" + money + "'"
            insert = insert + ")"
            sqlcommand = sqlcommand + "INSERT INTO SUB_BANK(BANK_NAME, CITY, POSSESSION) VALUES " + insert

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
#==============================================================================================
    if (rstype=="Delete"): # 删 #
        # Todo: 实现数据库操作，删除记录
        connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
        cursor = connection.cursor()

        primary = request.form['primary']
        primary = primary.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')

        sqlcommand = " SELECT * FROM EMPLOYEE WHERE "
        sqlcommand = sqlcommand + " EMPLOYEE_BANK_NAME = '" + primary + "'"
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
                                            'msg': '有关联员工信息'
                                            })
                                    )
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response
        
        sqlcommand = " SELECT * FROM LOAN WHERE "
        sqlcommand = sqlcommand + " BANK_NAME = '" + primary + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        # 使读取的 Oracle 数据字典化
        cursor.rowfactory = makeDictFactory(cursor)
        result = cursor.fetchall()
        if len(result) > 0 :
            cursor.close()
            connection.close()
            response = make_response(jsonify({    
                                            'code': 405,
                                            'msg': '有关联贷款信息'
                                            })
                                    )
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response

        sqlcommand = " SELECT * FROM CUSTOMER_CHECK_ACCOUNT WHERE "
        sqlcommand = sqlcommand + " BANK_NAME = '" + primary + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        # 使读取的 Oracle 数据字典化
        cursor.rowfactory = makeDictFactory(cursor)
        result = cursor.fetchall()
        if len(result) > 0 :
            cursor.close()
            connection.close()
            response = make_response(jsonify({    
                                            'code': 405,
                                            'msg': '有关联支票账户信息'
                                            })
                                    )
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response
        
        sqlcommand = " SELECT * FROM CUSTOMER_DEPOSIT_ACCOUNT WHERE "
        sqlcommand = sqlcommand + " BANK_NAME = '" + primary + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        # 使读取的 Oracle 数据字典化
        cursor.rowfactory = makeDictFactory(cursor)
        result = cursor.fetchall()
        if len(result) > 0 :
            cursor.close()
            connection.close()
            response = make_response(jsonify({    
                                            'code': 406,
                                            'msg': '有关联存款账户信息'
                                            })
                                    )
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response

        sqlcommand = " DELETE FROM SUB_BANK WHERE "
        sqlcommand = sqlcommand + " BANK_NAME = '" + primary + "'"
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