from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from flask_cors import *
import json
import time
import cx_Oracle

import os,sys
import math

from matplotlib import font_manager as fm
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from flask import Blueprint

summary_api = Blueprint('summary_api', __name__)
# Oracle 数据字典化函数
def makeDictFactory(cursor):
    columnNames = [d[0].lower() for d in cursor.description]
    def createRow(*args):
        return dict(zip(columnNames, args))
    return createRow
#-------------------------------    
#查找blist中是否出现a（年）eg.2018
def locate(a,blist):
    
    for i in range(len(blist)):
        if blist[i]['time'] == str(a):
            return i
    return -1
#------------------------------
#查找clist中是否出现a（年）b(month)  eg.2018 12

def locate_month(a,b,clist):
    combine_ab = str(a) + '.' + str(b)
    for i in range(len(clist)):
        if clist[i]['time'] == combine_ab:
            return i
    return -1
#------------------------------
#查找clist中是否出现a（年）b(month) 对应的季度 eg.2018 12

def locate_season(a,b,clist):
    s = math.ceil(b/3)
    season = str(a) + '-' + str(s)
    for i in range(len(clist)):
        if clist[i]['time'] == season:
            return i
    return -1
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
#=======================================================================================================
#=============按支行统计=============饼图-=============
#====================================================vv==========================
    if graphtype == 'pie':
    #==========================业务总金额=======================================
        if datatype == 'money':
            if sumtype == 'saving':
#           #==================================存储业务=======================================
# 支行1     支行2      支行3
# ￥233     ￥345     ￥678 （存储业务）
#
                #check account
                # sqlcommand = ""
                # sqlcommand = sqlcommand + " SELECT"
                # sqlcommand = sqlcommand + " BANK_NAME AS B_name1" + ','
                # sqlcommand = sqlcommand + " SUM(CHECK_ACCOUNT_MONEY) AS SUM_C_A_money"
                # sqlcommand = sqlcommand + " FROM"

                # sqlcommand = sqlcommand + "("
                # sqlcommand = sqlcommand + " SELECT"
                # sqlcommand = sqlcommand + " BANK_NAME AS B_name"   + ','
                # sqlcommand = sqlcommand + " CHECK_ACCOUNT_ID AS C_A_ID1"   + ','
                # sqlcommand = sqlcommand + " CHECK_ACCOUNT_MONEY AS C_A_money1"
                # sqlcommand = sqlcommand + " FROM"
                # sqlcommand = sqlcommand + "("
                # sqlcommand = sqlcommand + " SELECT"
                # sqlcommand = sqlcommand + " CHECK_ACCOUNT_ID AS C_A_ID"   + ','
                # sqlcommand = sqlcommand + " CHECK_ACCOUNT_MONEY AS C_A_money"
                # sqlcommand = sqlcommand + " FROM"
                # sqlcommand = sqlcommand + " CHECK_ACCOUNT"
                # sqlcommand = sqlcommand + " WHERE"  
                # if (len(lowerBound) > 0) :
                #     sqlcommand = sqlcommand + " AND CHECK_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                # if (len(upperBound) > 0) :
                #     sqlcommand = sqlcommand + " AND CHECK_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                # sqlcommand = sqlcommand + ")"
                # sqlcommand = sqlcommand + "NEW_CHECK_ACCOUNT" + ','
                # sqlcommand = sqlcommand + " CUSTOMER_CHECK_ACCOUNT"
                # sqlcommand = sqlcommand + " WHERE" 
                # sqlcommand = sqlcommand + " NEW_CHECK_ACCOUNT.CHECK_ACCOUNT_ID == CUSTOMER_CHECK_ACCOUNT.CHECK_ACCOUNT_ID" 
                # sqlcommand = sqlcommand + ")"

                # sqlcommand = sqlcommand + " GROUP BY"
                # sqlcommand = sqlcommand + " BANK_NAME"

                #---------check account-----------
                sqlcommand_check = ""
                sqlcommand_check_term = ""
                if (len(lowerBound) > 0) :
                    sqlcommand_check_term = sqlcommand_check_term + "  CHECK_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                if (len(upperBound) > 0) :
                    sqlcommand_check_term = sqlcommand_check_term + " AND CHECK_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                
                sqlcommand_check = sqlcommand_check + '''
                
                SELECT 
                    B_name AS B_name1, 
                    SUM(C_A_money1) AS SUM_C_A_money 
                FROM( 
                    SELECT 	CUSTOMER_CHECK_ACCOUNT.BANK_NAME AS B_name, 
                            NEW_CHECK_ACCOUNT.C_A_ID AS C_A_ID1, 
                            NEW_CHECK_ACCOUNT.C_A_money AS C_A_money1 
                    FROM( 
                            SELECT 
                                CHECK_ACCOUNT_ID AS C_A_ID, 
                                CHECK_ACCOUNT_MONEY AS C_A_money 
                            FROM CHECK_ACCOUNT 
                            WHERE ''' + sqlcommand_check_term + '''
                            )NEW_CHECK_ACCOUNT,
                    
                            CUSTOMER_CHECK_ACCOUNT 
                    WHERE NEW_CHECK_ACCOUNT.C_A_ID = CUSTOMER_CHECK_ACCOUNT.CHECK_ACCOUNT_ID
                    ) 
                    GROUP BY B_name
                '''
                print(sqlcommand_check)
                cursor.execute(sqlcommand_check)
                cursor.rowfactory = makeDictFactory(cursor)
                result_check = cursor.fetchall()
                
                print(result_check)
                #----------deposit account--------

                sqlcommand_deposit = ""
                sqlcommand_deposit_term = ""
                if (len(lowerBound) > 0) :
                    sqlcommand_deposit_term = sqlcommand_deposit_term + "  DEPOSIT_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                if (len(upperBound) > 0) :
                    sqlcommand_deposit_term = sqlcommand_deposit_term + " AND DEPOSIT_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                
                sqlcommand_deposit = sqlcommand_deposit + '''
                SELECT 
                    B_name AS B_name2, 
                    SUM(D_A_money1) AS SUM_D_A_money 
                FROM( 
                    SELECT 	CUSTOMER_DEPOSIT_ACCOUNT.BANK_NAME AS B_name, 
                            NEW_DEPOSIT_ACCOUNT.D_A_ID AS D_A_ID1, 
                            NEW_DEPOSIT_ACCOUNT.D_A_money AS D_A_money1 
                    FROM( 
                            SELECT 
                                DEPOSIT_ACCOUNT_ID AS D_A_ID, 
                                DEPOSIT_ACCOUNT_MONEY AS D_A_money 
                            FROM DEPOSIT_ACCOUNT 
                            WHERE '''+ sqlcommand_deposit_term +'''

                            )NEW_DEPOSIT_ACCOUNT,
                    
                            CUSTOMER_DEPOSIT_ACCOUNT 
                    WHERE NEW_DEPOSIT_ACCOUNT.D_A_ID = CUSTOMER_DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_ID
                    ) 
                    GROUP BY B_name
                '''
                print(sqlcommand_deposit)
                cursor.execute(sqlcommand_deposit)
                cursor.rowfactory = makeDictFactory(cursor)
                result_deposit = cursor.fetchall()
                
                print(result_deposit)

                #-----------合并储蓄账户和支票账户 查询结果------------ 

                columnlist_pie_money_saving = []
                rawData_pie_money_saving = {}
                for i in range(len(result_check)):
                    columnlist_pie_money_saving.append(result_check[i]['b_name1'])
                for i in range(len(result_deposit)):
                    if result_deposit[i]['b_name2'] not in columnlist_pie_money_saving:
                        columnlist_pie_money_saving.append(result_deposit[i]['b_name2'])

                print('columnlist_pie_money_saving is:')    
                print(columnlist_pie_money_saving) 

                
                for i in range(len(result_check)):
                    if result_check[i]['b_name1'] not in rawData_pie_money_saving:
                        rawData_pie_money_saving[result_check[i]['b_name1']] = result_check[i]['sum_c_a_money']
                    else:
                        rawData_pie_money_saving[result_check[i]['b_name1']] += result_check[i]['sum_c_a_money']
                
                for i in range(len(result_deposit)):
                    if result_deposit[i]['b_name2'] not in rawData_pie_money_saving:
                        rawData_pie_money_saving[result_deposit[i]['b_name2']] = result_deposit[i]['sum_d_a_money']
                    else:
                        rawData_pie_money_saving[result_deposit[i]['b_name2']] += result_deposit[i]['sum_d_a_money']

                print('rawData_pie_money_saving is:')
                print(rawData_pie_money_saving)

                #--------------饼状图----------------
                # plt.rcParams['font.sans-serif']=['SimHei'] 
                # keys = []
                # values = []

                # for i in range(len(columnlist_pie_money_saving)):
                #     values.append(rawData_pie_money_saving[columnlist_pie_money_saving[i]])
                # for i in range(len(columnlist_pie_money_saving)):
                #     keys.append(columnlist_pie_money_saving[i].strip())

                # print('ooooooooooooooooo---pie---oooooooooooo:')
                # print(columnlist_pie_money_saving)
                

                # s = pd.Series(values, index=keys)

                # labels = s.index
                # sizes = s.values

                # #fig1, ax1 = plt.subplots( figsize=(6,6)) # 设置绘图区域大小
                # fig1, ax1 = plt.subplots()
                # ax1.pie(sizes, labels=labels, autopct='%1.0f%%',
                #         shadow=True, startangle=190)

                # ax1.axis('equal')  

                # if os.path.exists(r'../static/summary.png'):
                #     os.remove(r'../static/summary.png')
                #     print('finish remove')
                # plt.savefig(r'../static/summary.png')
                # #plt.show() 
            #-------饼状图end-------------

                if result_check or result_deposit :
                    response = make_response(
                        jsonify(
                            {
                                'code': 200,
                                'columnList':columnlist_pie_money_saving,
                                    'rawData':[
                                        rawData_pie_money_saving                                   
                                    ]
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

            elif sumtype == 'loan':
        #=============================贷款业务==========================
#
# 支行1     支行2      支行3
# ￥233     ￥345     ￥678 （loan）
#

                sqlcommand_loan = ""
                sqlcommand_loan_term = ""
                if (len(lowerBound) > 0) :
                    sqlcommand_loan_term = sqlcommand_loan_term + " PAY_DATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                if (len(upperBound) > 0) :
                    sqlcommand_loan_term = sqlcommand_loan_term + " AND PAY_DATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                
                sqlcommand_loan = sqlcommand_loan + '''
                
                SELECT 
                    bank_name1 AS bank_name2, 
                    SUM(pay_money1) AS sum_pay_money2 
                FROM( 
                    SELECT 	NEW_PAY.loan_id0 AS loan_id1, 
                            NEW_PAY.pay_date0 AS pay_date1, 
                            NEW_PAY.pay_money0 AS pay_money1,
                            LOAN.BANK_NAME AS bank_name1 
                    FROM( 
                            SELECT 
                                LOAN_ID AS loan_id0, 
                                PAY_DATE AS pay_date0, 
                                PAY_MONEY AS pay_money0
                            FROM PAY 
                            WHERE ''' + sqlcommand_loan_term + '''
                        )NEW_PAY, LOAN

                    WHERE NEW_PAY.loan_id0 = LOAN.LOAN_ID
                    ) 
                    GROUP BY bank_name1
                '''
                print(sqlcommand_loan)
                cursor.execute(sqlcommand_loan)
                cursor.rowfactory = makeDictFactory(cursor)
                result_loan = cursor.fetchall()
                
                print(result_loan)
                #--------结果处理---------
                columnlist_pie_money_loan = []
                rawData_pie_money_loan = {}

                for i in range(len(result_loan)):
                    columnlist_pie_money_loan.append(result_loan[i]['bank_name2'])
                print('columnlist_pie_money_loan is:')    
                print(columnlist_pie_money_loan)    

                for i in range(len(result_loan)):
                    rawData_pie_money_loan[result_loan[i]['bank_name2']] =  result_loan[i]['sum_pay_money2']              

                print('rawData_pie_money_loan is:')
                print(rawData_pie_money_loan)

                #-------------饼状图-------------------
                # plt.rcParams['font.sans-serif']=['SimHei'] 
                # values = []
                # keys = []
                # for i in range(len(columnlist_pie_money_loan)):
                #     values.append(rawData_pie_money_loan[columnlist_pie_money_loan[i]])
                # for i in range(len(columnlist_pie_money_loan)):
                #     keys.append( columnlist_pie_money_loan[i].strip() )

                # print('ooooooooooooooooo---pie---oooooooooooo:')
                # print(columnlist_pie_money_loan)
                

                # s = pd.Series(values, index=keys)

                # labels = s.index
                # sizes = s.values

                # #fig1, ax1 = plt.subplots( figsize=(6,6)) # 设置绘图区域大小
                # fig1, ax1 = plt.subplots()
                # ax1.pie(sizes, labels=labels, autopct='%1.0f%%',
                #         shadow=True, startangle=190)

                # ax1.axis('equal')  
                # if os.path.exists(r'../static/summary.png'):
                #     os.remove(r'../static/summary.png')
                #     print('finish remove')
                # plt.savefig(r'../static/summary.png')
                #plt.show() 
                #------------end---------------------


                if result_loan :
                    response = make_response(
                        jsonify(
                            {
                                'code': 200,
                                'columnList':columnlist_pie_money_loan,
                                    'rawData':[
                                        rawData_pie_money_loan                                   
                                    ]
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

            elif sumtype == 'all':#所有业务
#
# 支行1     支行2      支行3
# ￥233     ￥345     ￥678 （all）
#                
                #------no.1---loan--------

                sqlcommand_loan = ""
                sqlcommand_loan_term = ""
                if (len(lowerBound) > 0) :
                    sqlcommand_loan_term = sqlcommand_loan_term + " PAY_DATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                if (len(upperBound) > 0) :
                    sqlcommand_loan_term = sqlcommand_loan_term + " AND PAY_DATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                
                sqlcommand_loan = sqlcommand_loan + '''
                
                SELECT 
                    bank_name1 AS bank_name2, 
                    SUM(pay_money1) AS sum_pay_money2 
                FROM( 
                    SELECT 	NEW_PAY.loan_id0 AS loan_id1, 
                            NEW_PAY.pay_date0 AS pay_date1, 
                            NEW_PAY.pay_money0 AS pay_money1,
                            LOAN.BANK_NAME AS bank_name1 
                    FROM( 
                            SELECT 
                                LOAN_ID AS loan_id0, 
                                PAY_DATE AS pay_date0, 
                                PAY_MONEY AS pay_money0
                            FROM PAY 
                            WHERE ''' + sqlcommand_loan_term + '''
                        )NEW_PAY, LOAN

                    WHERE NEW_PAY.loan_id0 = LOAN.LOAN_ID
                    ) 
                    GROUP BY bank_name1
                '''
                print(sqlcommand_loan)
                cursor.execute(sqlcommand_loan)
                cursor.rowfactory = makeDictFactory(cursor)
                result_loan = cursor.fetchall()
                
                print(result_loan)

                #------no.2---check--------

                sqlcommand_check = ""
                sqlcommand_check_term = ""
                if (len(lowerBound) > 0) :
                    sqlcommand_check_term = sqlcommand_check_term + "  CHECK_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                if (len(upperBound) > 0) :
                    sqlcommand_check_term = sqlcommand_check_term + " AND CHECK_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                
                sqlcommand_check = sqlcommand_check + '''
                
                SELECT 
                    B_name AS B_name1, 
                    SUM(C_A_money1) AS SUM_C_A_money 
                FROM( 
                    SELECT 	CUSTOMER_CHECK_ACCOUNT.BANK_NAME AS B_name, 
                            NEW_CHECK_ACCOUNT.C_A_ID AS C_A_ID1, 
                            NEW_CHECK_ACCOUNT.C_A_money AS C_A_money1 
                    FROM( 
                            SELECT 
                                CHECK_ACCOUNT_ID AS C_A_ID, 
                                CHECK_ACCOUNT_MONEY AS C_A_money 
                            FROM CHECK_ACCOUNT 
                            WHERE ''' + sqlcommand_check_term + '''
                            )NEW_CHECK_ACCOUNT,
                    
                            CUSTOMER_CHECK_ACCOUNT 
                    WHERE NEW_CHECK_ACCOUNT.C_A_ID = CUSTOMER_CHECK_ACCOUNT.CHECK_ACCOUNT_ID
                    ) 
                    GROUP BY B_name
                '''
                print(sqlcommand_check)
                cursor.execute(sqlcommand_check)
                cursor.rowfactory = makeDictFactory(cursor)
                result_check = cursor.fetchall()
                
                print(result_check)

                #------no.3---deposit--------

                sqlcommand_deposit = ""
                sqlcommand_deposit_term = ""
                if (len(lowerBound) > 0) :
                    sqlcommand_deposit_term = sqlcommand_deposit_term + "  DEPOSIT_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                if (len(upperBound) > 0) :
                    sqlcommand_deposit_term = sqlcommand_deposit_term + " AND DEPOSIT_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                
                sqlcommand_deposit = sqlcommand_deposit + '''
                SELECT 
                    B_name AS B_name2, 
                    SUM(D_A_money1) AS SUM_D_A_money 
                FROM( 
                    SELECT 	CUSTOMER_DEPOSIT_ACCOUNT.BANK_NAME AS B_name, 
                            NEW_DEPOSIT_ACCOUNT.D_A_ID AS D_A_ID1, 
                            NEW_DEPOSIT_ACCOUNT.D_A_money AS D_A_money1 
                    FROM( 
                            SELECT 
                                DEPOSIT_ACCOUNT_ID AS D_A_ID, 
                                DEPOSIT_ACCOUNT_MONEY AS D_A_money 
                            FROM DEPOSIT_ACCOUNT 
                            WHERE '''+ sqlcommand_deposit_term +'''

                            )NEW_DEPOSIT_ACCOUNT,
                    
                            CUSTOMER_DEPOSIT_ACCOUNT 
                    WHERE NEW_DEPOSIT_ACCOUNT.D_A_ID = CUSTOMER_DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_ID
                    ) 
                    GROUP BY B_name
                '''
                print(sqlcommand_deposit)
                cursor.execute(sqlcommand_deposit)
                cursor.rowfactory = makeDictFactory(cursor)
                result_deposit = cursor.fetchall()
                
                print(result_deposit)

                #--------结果处理---------
                columnlist_pie_money_all = []
                rawData_pie_money_all = {}

                for i in range(len(result_loan)):
                    columnlist_pie_money_all.append(result_loan[i]['bank_name2'])    
      
                for i in range(len(result_check)):
                    if result_deposit[i]['b_name2'] not in columnlist_pie_money_all:
                        columnlist_pie_money_all.append(result_check[i]['b_name1'])

                for i in range(len(result_deposit)):
                    if result_deposit[i]['b_name2'] not in columnlist_pie_money_all:
                        columnlist_pie_money_all.append(result_deposit[i]['b_name2'])

                print('columnlist_pie_money_all is:')    
                print(columnlist_pie_money_all) 


                for i in range(len(result_loan)):
                    if result_loan[i]['bank_name2'] not in rawData_pie_money_all:
                        rawData_pie_money_all[result_loan[i]['bank_name2']] =  result_loan[i]['sum_pay_money2']              
                    else:
                        rawData_pie_money_all[result_loan[i]['bank_name2']] += result_loan[i]['sum_pay_money2']
                
                for i in range(len(result_check)):
                    if result_check[i]['b_name1'] not in rawData_pie_money_all:
                        rawData_pie_money_all[result_check[i]['b_name1']] = result_check[i]['sum_c_a_money']
                    else:
                        rawData_pie_money_all[result_check[i]['b_name1']] += result_check[i]['sum_c_a_money']
                
                for i in range(len(result_deposit)):
                    if result_deposit[i]['b_name2'] not in rawData_pie_money_all:
                        rawData_pie_money_all[result_deposit[i]['b_name2']] = result_deposit[i]['sum_d_a_money']
                    else:
                        rawData_pie_money_all[result_deposit[i]['b_name2']] += result_deposit[i]['sum_d_a_money']

                print('rawData_pie_money_all is:')
                print(rawData_pie_money_all)

                #-------------饼状图-------------------
                # plt.rcParams['font.sans-serif']=['SimHei'] 
                # values = []
                # keys = []
                # for i in range(len(columnlist_pie_money_all)):
                #     values.append(rawData_pie_money_all[columnlist_pie_money_all[i]])
                # for i in range(len(columnlist_pie_money_all)):
                #     keys.append(columnlist_pie_money_all[i].strip()) 

                

                # s = pd.Series(values, index=keys)

                # labels = s.index
                # sizes = s.values

                # #fig1, ax1 = plt.subplots( figsize=(6,6)) # 设置绘图区域大小
                # fig1, ax1 = plt.subplots()
                # ax1.pie(sizes, labels=labels, autopct='%1.0f%%',
                #         shadow=True, startangle=190)

                # ax1.axis('equal')  
                # if os.path.exists(r'../static/summary.png'):
                #     os.remove(r'../static/summary.png')
                #     print('finish remove')
                # plt.savefig(r'../static/summary.png')
                # #plt.show() 
                #------------end---------------------

                if result_loan or result_check or result_deposit :
                    response = make_response(
                        jsonify(
                            {
                                'code': 200,
                                'columnList':columnlist_pie_money_all,
                                    'rawData':[
                                        rawData_pie_money_all                                   
                                    ]
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

        elif  datatype == 'user':
    #=======================================用户数=======================================
    
#
# 支行1     支行2      支行3
#  5人      10人        8人 （存储业务）
#           
            #==========================用户统计=============存储业务==========================
            if sumtype == 'saving':
                #-------check-----account-----
                sqlcommand_check = ""
                sqlcommand_check_term = ""
                if (len(lowerBound) > 0) :
                    sqlcommand_check_term = sqlcommand_check_term + "  CHECK_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                if (len(upperBound) > 0) :
                    sqlcommand_check_term = sqlcommand_check_term + " AND CHECK_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                
                sqlcommand_check = sqlcommand_check + '''
                
                SELECT 
                    B_name AS B_name1, 
                    COUNT( distinct  customer_id) AS count_customer1 
                FROM( 
                    SELECT 	CUSTOMER_CHECK_ACCOUNT.BANK_NAME AS B_name, 
                            CUSTOMER_CHECK_ACCOUNT.CUSTOMER_ID AS customer_id,
                            NEW_CHECK_ACCOUNT.C_A_ID AS C_A_ID1
                                                    
                    FROM( 
                            SELECT 
                                CHECK_ACCOUNT_ID AS C_A_ID

                            FROM CHECK_ACCOUNT 
                            WHERE ''' + sqlcommand_check_term + '''
                            )NEW_CHECK_ACCOUNT,  CUSTOMER_CHECK_ACCOUNT 

                    WHERE NEW_CHECK_ACCOUNT.C_A_ID = CUSTOMER_CHECK_ACCOUNT.CHECK_ACCOUNT_ID
                    ) 
                    GROUP BY B_name
                '''
                print(sqlcommand_check)
                cursor.execute(sqlcommand_check)
                cursor.rowfactory = makeDictFactory(cursor)
                result_check = cursor.fetchall()
                
                print(result_check)
                #----------deposit account--------

                sqlcommand_deposit = ""
                sqlcommand_deposit_term = ""
                if (len(lowerBound) > 0) :
                    sqlcommand_deposit_term = sqlcommand_deposit_term + "  DEPOSIT_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                if (len(upperBound) > 0) :
                    sqlcommand_deposit_term = sqlcommand_deposit_term + " AND DEPOSIT_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                
                sqlcommand_deposit = sqlcommand_deposit + '''
                SELECT 
                    B_name AS B_name2, 
                    COUNT( distinct customer_id) AS count_customer2 
                FROM( 
                    SELECT 	CUSTOMER_DEPOSIT_ACCOUNT.BANK_NAME AS B_name, 
                            CUSTOMER_DEPOSIT_ACCOUNT.CUSTOMER_ID AS customer_id,
                            NEW_DEPOSIT_ACCOUNT.D_A_ID AS D_A_ID1

                    FROM( 
                            SELECT 
                                DEPOSIT_ACCOUNT_ID AS D_A_ID
                            FROM DEPOSIT_ACCOUNT 
                            WHERE '''+ sqlcommand_deposit_term +'''

                            )NEW_DEPOSIT_ACCOUNT,CUSTOMER_DEPOSIT_ACCOUNT

                    WHERE NEW_DEPOSIT_ACCOUNT.D_A_ID = CUSTOMER_DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_ID
                    ) 
                    GROUP BY B_name
                '''
                print(sqlcommand_deposit)
                cursor.execute(sqlcommand_deposit)
                cursor.rowfactory = makeDictFactory(cursor)
                result_deposit = cursor.fetchall()
                
                print(result_deposit)

                #=============用户统计=============储蓄业务-----结果处理-----------
                columnlist_pie_user_saving = []
                rawData_pie_user_saving = {}
                for i in range(len(result_check)):
                    columnlist_pie_user_saving.append(result_check[i]['b_name1'])
                for i in range(len(result_deposit)):
                    if result_deposit[i]['b_name2'] not in columnlist_pie_user_saving:
                        columnlist_pie_user_saving.append(result_deposit[i]['b_name2'])

                print('columnlist_pie_user_saving is:')    
                print(columnlist_pie_user_saving) 

                
                for i in range(len(result_check)):
                    if result_check[i]['b_name1'] not in rawData_pie_user_saving:
                        rawData_pie_user_saving[result_check[i]['b_name1']] = result_check[i]['count_customer1']
                    else:
                        rawData_pie_user_saving[result_check[i]['b_name1']] += result_check[i]['count_customer1']
                
                for i in range(len(result_deposit)):
                    if result_deposit[i]['b_name2'] not in rawData_pie_user_saving:
                        rawData_pie_user_saving[result_deposit[i]['b_name2']] = result_deposit[i]['count_customer2']
                    else:
                        rawData_pie_user_saving[result_deposit[i]['b_name2']] += result_deposit[i]['count_customer2']

                print('rawData_pie_user_saving is:')
                print(rawData_pie_user_saving)


                if result_check or result_deposit :
                    response = make_response(
                        jsonify(
                            {
                                'code': 200,
                                'columnList':columnlist_pie_user_saving,
                                    'rawData':[
                                        rawData_pie_user_saving                                   
                                    ]
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

            #---------  
#
# 支行1     支行2      支行3
#  5人      10人        8人 （贷款业务）
#           
            #=============用户统计=============贷款业务=============:
            elif sumtype == 'loan':
                sqlcommand_loan = ""
                sqlcommand_loan_term = ""
                if (len(lowerBound) > 0) :
                    sqlcommand_loan_term = sqlcommand_loan_term + " PAY_DATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                if (len(upperBound) > 0) :
                    sqlcommand_loan_term = sqlcommand_loan_term + " AND PAY_DATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                
                sqlcommand_loan = sqlcommand_loan + '''
                
                SELECT 
                    bank_name1 AS bank_name3, 
                    COUNT( distinct  customer_id) AS count_customer3
                FROM( 
                    SELECT 	NEW_PAY.loan_id0 AS loan_id1, 
                            LOAN_CUSTOMER.CUSTOMER_ID AS customer_id,
                            LOAN.BANK_NAME AS bank_name1 
                    FROM( 
                            SELECT 
                                LOAN_ID AS loan_id0

                            FROM PAY 
                            WHERE ''' + sqlcommand_loan_term + '''
                        )NEW_PAY, LOAN, LOAN_CUSTOMER

                    WHERE NEW_PAY.loan_id0 = LOAN.LOAN_ID and NEW_PAY.loan_id0 = LOAN_CUSTOMER.LOAN_ID
                    ) 
                    GROUP BY bank_name1
                '''
                print(sqlcommand_loan)
                cursor.execute(sqlcommand_loan)
                cursor.rowfactory = makeDictFactory(cursor)
                result_loan = cursor.fetchall()
                
                print(result_loan)

                #-------用户统计----贷款业务-------结果处理---------

                columnlist_pie_user_loan = []
                rawData_pie_user_loan = {}

                for i in range(len(result_loan)):
                    columnlist_pie_user_loan.append(result_loan[i]['bank_name3'])
                print('columnlist_pie_user_loan is:')    
                print(columnlist_pie_user_loan)    

                for i in range(len(result_loan)):
                    rawData_pie_user_loan[result_loan[i]['bank_name3']] =  result_loan[i]['count_customer3']              

                print('rawData_pie_user_loan is:')
                print(rawData_pie_user_loan)


                if result_loan :
                    response = make_response(
                        jsonify(
                            {
                                'code': 200,
                                'columnList':columnlist_pie_user_loan,
                                    'rawData':[
                                        rawData_pie_user_loan                                   
                                    ]
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
#
# 支行1     支行2      支行3
#  5人      10人        8人 （all业务）
            elif sumtype == 'all':
            #-------用户统计----all业务---------:

              #------------no.1-------check--------
                sqlcommand_check = ""
                sqlcommand_check_term = ""
                if (len(lowerBound) > 0) :
                    sqlcommand_check_term = sqlcommand_check_term + "  CHECK_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                if (len(upperBound) > 0) :
                    sqlcommand_check_term = sqlcommand_check_term + " AND CHECK_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                
                sqlcommand_check = sqlcommand_check + '''
                
                SELECT 
                    B_name AS B_name1, 
                    COUNT( distinct  customer_id) AS count_customer1 
                FROM( 
                    SELECT 	CUSTOMER_CHECK_ACCOUNT.BANK_NAME AS B_name, 
                            CUSTOMER_CHECK_ACCOUNT.CUSTOMER_ID AS customer_id,
                            NEW_CHECK_ACCOUNT.C_A_ID AS C_A_ID1
                                                    
                    FROM( 
                            SELECT 
                                CHECK_ACCOUNT_ID AS C_A_ID

                            FROM CHECK_ACCOUNT 
                            WHERE ''' + sqlcommand_check_term + '''
                            )NEW_CHECK_ACCOUNT,  CUSTOMER_CHECK_ACCOUNT 

                    WHERE NEW_CHECK_ACCOUNT.C_A_ID = CUSTOMER_CHECK_ACCOUNT.CHECK_ACCOUNT_ID
                    ) 
                    GROUP BY B_name
                '''
                print(sqlcommand_check)
                cursor.execute(sqlcommand_check)
                cursor.rowfactory = makeDictFactory(cursor)
                result_check = cursor.fetchall()
                
                print(result_check)

                #-----------no.2--------deposit-----------

                sqlcommand_deposit = ""
                sqlcommand_deposit_term = ""
                if (len(lowerBound) > 0) :
                    sqlcommand_deposit_term = sqlcommand_deposit_term + "  DEPOSIT_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                if (len(upperBound) > 0) :
                    sqlcommand_deposit_term = sqlcommand_deposit_term + " AND DEPOSIT_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                
                sqlcommand_deposit = sqlcommand_deposit + '''
                SELECT 
                    B_name AS B_name2, 
                    COUNT( distinct  customer_id) AS count_customer2 
                FROM( 
                    SELECT 	CUSTOMER_DEPOSIT_ACCOUNT.BANK_NAME AS B_name, 
                            CUSTOMER_DEPOSIT_ACCOUNT.CUSTOMER_ID AS customer_id,
                            NEW_DEPOSIT_ACCOUNT.D_A_ID AS D_A_ID1

                    FROM( 
                            SELECT 
                                DEPOSIT_ACCOUNT_ID AS D_A_ID
                            FROM DEPOSIT_ACCOUNT 
                            WHERE '''+ sqlcommand_deposit_term +'''

                            )NEW_DEPOSIT_ACCOUNT,CUSTOMER_DEPOSIT_ACCOUNT

                    WHERE NEW_DEPOSIT_ACCOUNT.D_A_ID = CUSTOMER_DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_ID
                    ) 
                    GROUP BY B_name
                '''
                print(sqlcommand_deposit)
                cursor.execute(sqlcommand_deposit)
                cursor.rowfactory = makeDictFactory(cursor)
                result_deposit = cursor.fetchall()
                
                print(result_deposit)

                #-----------no.3---------loan------

                sqlcommand_loan = ""
                sqlcommand_loan_term = ""
                if (len(lowerBound) > 0) :
                    sqlcommand_loan_term = sqlcommand_loan_term + " PAY_DATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                if (len(upperBound) > 0) :
                    sqlcommand_loan_term = sqlcommand_loan_term + " AND PAY_DATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                
                sqlcommand_loan = sqlcommand_loan + '''
                
                SELECT 
                    bank_name1 AS bank_name3, 
                    COUNT( distinct  customer_id) AS count_customer3
                FROM( 
                    SELECT 	NEW_PAY.loan_id0 AS loan_id1, 
                            LOAN_CUSTOMER.CUSTOMER_ID AS customer_id,
                            LOAN.BANK_NAME AS bank_name1 
                    FROM( 
                            SELECT 
                                LOAN_ID AS loan_id0

                            FROM PAY 
                            WHERE ''' + sqlcommand_loan_term + '''
                        )NEW_PAY, LOAN, LOAN_CUSTOMER

                    WHERE NEW_PAY.loan_id0 = LOAN.LOAN_ID and NEW_PAY.loan_id0 = LOAN_CUSTOMER.LOAN_ID
                    ) 
                    GROUP BY bank_name1
                '''
                print(sqlcommand_loan)
                cursor.execute(sqlcommand_loan)
                cursor.rowfactory = makeDictFactory(cursor)
                result_loan = cursor.fetchall()
                
                print(result_loan)

                #-------用户统计-----all----结果处理---------

                columnlist_pie_user_all = []
                rawData_pie_user_all = {}

                for i in range(len(result_loan)):
                    columnlist_pie_user_all.append(result_loan[i]['bank_name3'])
 
                for i in range(len(result_check)):
                    if result_check[i]['b_name1'] not in columnlist_pie_user_all:
                        columnlist_pie_user_all.append(result_check[i]['b_name1'])

                for i in range(len(result_deposit)):
                    if result_deposit[i]['b_name2'] not in columnlist_pie_user_all:
                        columnlist_pie_user_all.append(result_deposit[i]['b_name2'])

                print('columnlist_pie_user_all is:')    
                print(columnlist_pie_user_all) 

                
                for i in range(len(result_check)):
                    if result_check[i]['b_name1'] not in rawData_pie_user_all:
                        rawData_pie_user_all[result_check[i]['b_name1']] = result_check[i]['count_customer1']
                    else:
                        rawData_pie_user_all[result_check[i]['b_name1']] += result_check[i]['count_customer1']
                
                for i in range(len(result_deposit)):
                    if result_deposit[i]['b_name2'] not in rawData_pie_user_all:
                        rawData_pie_user_all[result_deposit[i]['b_name2']] = result_deposit[i]['count_customer2']
                    else:
                        rawData_pie_user_all[result_deposit[i]['b_name2']] += result_deposit[i]['count_customer2']
                
                for i in range(len(result_loan)):
                    if result_loan[i]['bank_name3'] not in rawData_pie_user_all:
                        rawData_pie_user_all[result_loan[i]['bank_name3']] =  result_loan[i]['count_customer3']
                    else:
                        rawData_pie_user_all[result_loan[i]['bank_name3']] +=  result_loan[i]['count_customer3']
                
                print('rawData_pie_user_all is:')
                print(rawData_pie_user_all)
               
                #-------------饼状图-------------------
                # plt.rcParams['font.sans-serif']=['SimHei'] 
                # values = []
                # keys = []
                # for i in range(len(columnlist_pie_user_all)):
                #     values.append(rawData_pie_user_all[columnlist_pie_user_all[i]])
                # for i in range(len(columnlist_pie_user_all)):
                #     keys.append(columnlist_pie_user_all[i].strip())

                

                # s = pd.Series(values, index=keys)

                # labels = s.index
                # sizes = s.values

                # #fig1, ax1 = plt.subplots( figsize=(6,6)) # 设置绘图区域大小
                # fig1, ax1 = plt.subplots()
                # ax1.pie(sizes, labels=labels, autopct='%1.0f%%',
                #         shadow=True, startangle=190)

                # ax1.axis('equal')  
                # if os.path.exists(r'../static/summary.png'):
                #     os.remove(r'../static/summary.png')
                #     print('finish remove')
                # plt.savefig(r'../static/summary.png')
                # #plt.show()
                #------------end---------------------

                if result_loan or result_check or result_deposit :
                    response = make_response(
                        jsonify(
                            {
                                'code': 200,
                                'columnList':columnlist_pie_user_all,
                                    'rawData':[
                                        rawData_pie_user_all                                   
                                    ]
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
    else:


        #===================================================================================================
        #--------按时间统计---------折线图-------
        #===================================================================================================



    #=======================================业务总金额======================================================================
        if datatype == 'money':

            #===================================存储业务==================================================================
            if sumtype == 'saving':
                #===============================以年为粒度=====================================================================
                if timegrain == 'year':#---

                    sqlcommand_check = ""
                    sqlcommand_check_term = ""
                    if (len(lowerBound) > 0) :
                        sqlcommand_check_term = sqlcommand_check_term + "  CHECK_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                    if (len(upperBound) > 0) :
                        sqlcommand_check_term = sqlcommand_check_term + " AND CHECK_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                    
                    sqlcommand_check = sqlcommand_check + '''
                    
                        SELECT 	CUSTOMER_CHECK_ACCOUNT.BANK_NAME AS B_name1,                                  
                                NEW_CHECK_ACCOUNT.C_A_money AS C_A_money1,
                                NEW_CHECK_ACCOUNT.C_A_date AS C_A_date1

                        FROM( 
                                SELECT 
                                    CHECK_ACCOUNT_ID AS C_A_ID, 
                                    CHECK_ACCOUNT_MONEY AS C_A_money,
                                    CHECK_ACCOUNT_REGDATE AS  C_A_date
                                FROM CHECK_ACCOUNT 
                                WHERE ''' + sqlcommand_check_term + '''
                                )NEW_CHECK_ACCOUNT,
                        
                                CUSTOMER_CHECK_ACCOUNT 
                        WHERE NEW_CHECK_ACCOUNT.C_A_ID = CUSTOMER_CHECK_ACCOUNT.CHECK_ACCOUNT_ID
                        ORDER BY NEW_CHECK_ACCOUNT.C_A_date ASC
      
                    '''
                    print(sqlcommand_check)
                    cursor.execute(sqlcommand_check)
                    cursor.rowfactory = makeDictFactory(cursor)
                    result_check = cursor.fetchall()
                    
                    print(result_check)

                    columnList = []
                    rawData = []

                    for i in range(len(result_check)):
                        if result_check[i]['b_name1'] not in columnList:
                            columnList.append(result_check[i]['b_name1'])
                    
                    for i in range(len(result_check)):
                        loc = locate(result_check[i]['c_a_date1'].year, rawData)
                        if  loc == -1 :
                            #如果这是 rawdata中没有的 一年
                            term = {}
                            term['time'] = str(result_check[i]['c_a_date1'].year)
                            term[result_check[i]['b_name1']] = result_check[i]['c_a_money1']
                            rawData.append(term)

                        else:
                            if result_check[i]['b_name1'] not in rawData[loc]:
                                #rawdata中有这一年  但是没有这条记录所在的支行  添加支行
                                rawData[loc][result_check[i]['b_name1']] = result_check[i]['c_a_money1']
                            else:
                                rawData[loc][result_check[i]['b_name1']] += result_check[i]['c_a_money1']
                    
                    

                    #----------deposit account--------

                    sqlcommand_deposit = ""
                    sqlcommand_deposit_term = ""
                    if (len(lowerBound) > 0) :
                        sqlcommand_deposit_term = sqlcommand_deposit_term + "  DEPOSIT_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                    if (len(upperBound) > 0) :
                        sqlcommand_deposit_term = sqlcommand_deposit_term + " AND DEPOSIT_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                    
                    sqlcommand_deposit = sqlcommand_deposit + '''
                    
                        SELECT 	CUSTOMER_DEPOSIT_ACCOUNT.BANK_NAME AS B_name2,                                  
                                NEW_DEPOSIT_ACCOUNT.D_A_money AS D_A_money1,
                                NEW_DEPOSIT_ACCOUNT.D_A_date AS D_A_date1

                        FROM( 
                                SELECT 
                                    DEPOSIT_ACCOUNT_ID AS D_A_ID, 
                                    DEPOSIT_ACCOUNT_MONEY AS D_A_money,
                                    DEPOSIT_ACCOUNT_REGDATE AS  D_A_date
                                FROM DEPOSIT_ACCOUNT 
                                WHERE ''' + sqlcommand_deposit_term + '''
                                )NEW_DEPOSIT_ACCOUNT,
                        
                                CUSTOMER_DEPOSIT_ACCOUNT 
                        WHERE NEW_DEPOSIT_ACCOUNT.D_A_ID = CUSTOMER_DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_ID
                        ORDER BY NEW_DEPOSIT_ACCOUNT.D_A_date ASC
      
                    '''
                    print(sqlcommand_deposit)
                    cursor.execute(sqlcommand_deposit)
                    cursor.rowfactory = makeDictFactory(cursor)
                    result_deposit = cursor.fetchall()
                    
                    print(result_deposit)

                    for i in range(len(result_deposit)):
                        if result_deposit[i]['b_name2'] not in columnList:
                            columnList.append(result_deposit[i]['b_name2'])
                    
                    for i in range(len(result_deposit)):
                        loc = locate(result_deposit[i]['d_a_date1'].year, rawData)
                        if  loc == -1 :
                            #如果这是 rawdata中没有的 一年
                            term = {}
                            term['time'] = str(result_deposit[i]['d_a_date1'].year)
                            term[result_deposit[i]['b_name2']] = result_deposit[i]['d_a_money1']
                            rawData.append(term)

                        else:
                            if result_deposit[i]['b_name2'] not in rawData[loc]:
                                #rawdata中有这一年  但是没有这条记录所在的支行  添加支行
                                rawData[loc][result_deposit[i]['b_name2']] = result_deposit[i]['d_a_money1']
                            else:
                                rawData[loc][result_deposit[i]['b_name2']] += result_deposit[i]['d_a_money1']
                    
                    if  result_check or result_deposit :
                        response = make_response(
                            jsonify(
                                {
                                    'code': 200,
                                    'columnList':columnList,
                                        'rawData': rawData
                                                                        
                                        
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

                elif timegrain == 'month':
            #===============================以month为粒度=========================================================
                    sqlcommand_check = ""
                    sqlcommand_check_term = ""
                    if (len(lowerBound) > 0) :
                        sqlcommand_check_term = sqlcommand_check_term + "  CHECK_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                    if (len(upperBound) > 0) :
                        sqlcommand_check_term = sqlcommand_check_term + " AND CHECK_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                    
                    sqlcommand_check = sqlcommand_check + '''
                    
                        SELECT 	CUSTOMER_CHECK_ACCOUNT.BANK_NAME AS B_name1,                                  
                                NEW_CHECK_ACCOUNT.C_A_money AS C_A_money1,
                                NEW_CHECK_ACCOUNT.C_A_date AS C_A_date1

                        FROM( 
                                SELECT 
                                    CHECK_ACCOUNT_ID AS C_A_ID, 
                                    CHECK_ACCOUNT_MONEY AS C_A_money,
                                    CHECK_ACCOUNT_REGDATE AS  C_A_date
                                FROM CHECK_ACCOUNT 
                                WHERE ''' + sqlcommand_check_term + '''
                                )NEW_CHECK_ACCOUNT,
                        
                                CUSTOMER_CHECK_ACCOUNT 
                        WHERE NEW_CHECK_ACCOUNT.C_A_ID = CUSTOMER_CHECK_ACCOUNT.CHECK_ACCOUNT_ID
                        ORDER BY NEW_CHECK_ACCOUNT.C_A_date ASC
      
                    '''
                    print(sqlcommand_check)
                    cursor.execute(sqlcommand_check)
                    cursor.rowfactory = makeDictFactory(cursor)
                    result_check = cursor.fetchall()
                    
                    print(result_check)

                    columnList = []
                    rawData = []

                    for i in range(len(result_check)):
                        if result_check[i]['b_name1'] not in columnList:
                            columnList.append(result_check[i]['b_name1'])
                    
                    for i in range(len(result_check)):
                        loc = locate_month(result_check[i]['c_a_date1'].year,result_check[i]['c_a_date1'].month, rawData)
                        if  loc == -1 :
                            #如果这是 rawdata中没有的 年+月
                            term = {}
                            yyyy_mm = str(result_check[i]['c_a_date1'].year) + '.' + str(result_check[i]['c_a_date1'].month) 
                            term['time'] = yyyy_mm
                            term[result_check[i]['b_name1']] = result_check[i]['c_a_money1']
                            rawData.append(term)

                        else:
                            if result_check[i]['b_name1'] not in rawData[loc]:
                                #rawdata中有这一年  但是没有这条记录所在的支行  添加支行
                                rawData[loc][result_check[i]['b_name1']] = result_check[i]['c_a_money1']
                            else:
                                rawData[loc][result_check[i]['b_name1']] += result_check[i]['c_a_money1']
                    
                    

                    #----------deposit account--------

                    sqlcommand_deposit = ""
                    sqlcommand_deposit_term = ""
                    if (len(lowerBound) > 0) :
                        sqlcommand_deposit_term = sqlcommand_deposit_term + "  DEPOSIT_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                    if (len(upperBound) > 0) :
                        sqlcommand_deposit_term = sqlcommand_deposit_term + " AND DEPOSIT_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                    
                    sqlcommand_deposit = sqlcommand_deposit + '''
                    
                        SELECT 	CUSTOMER_DEPOSIT_ACCOUNT.BANK_NAME AS B_name2,                                  
                                NEW_DEPOSIT_ACCOUNT.D_A_money AS D_A_money1,
                                NEW_DEPOSIT_ACCOUNT.D_A_date AS D_A_date1

                        FROM( 
                                SELECT 
                                    DEPOSIT_ACCOUNT_ID AS D_A_ID, 
                                    DEPOSIT_ACCOUNT_MONEY AS D_A_money,
                                    DEPOSIT_ACCOUNT_REGDATE AS  D_A_date
                                FROM DEPOSIT_ACCOUNT 
                                WHERE ''' + sqlcommand_deposit_term + '''
                                )NEW_DEPOSIT_ACCOUNT,
                        
                                CUSTOMER_DEPOSIT_ACCOUNT 
                        WHERE NEW_DEPOSIT_ACCOUNT.D_A_ID = CUSTOMER_DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_ID
                        ORDER BY NEW_DEPOSIT_ACCOUNT.D_A_date ASC
      
                    '''
                    print(sqlcommand_deposit)
                    cursor.execute(sqlcommand_deposit)
                    cursor.rowfactory = makeDictFactory(cursor)
                    result_deposit = cursor.fetchall()
                    
                    print(result_deposit)

                    for i in range(len(result_deposit)):
                        if result_deposit[i]['b_name2'] not in columnList:
                            columnList.append(result_deposit[i]['b_name2'])
                    
                    for i in range(len(result_deposit)):
                        loc = locate_month(result_deposit[i]['d_a_date1'].year, result_deposit[i]['d_a_date1'].month, rawData)
                        if  loc == -1 :
                            #如果这是 rawdata中没有的 一年
                            term = {}
                            yyyy_mm = str(result_deposit[i]['d_a_date1'].year) + '.' + str(result_deposit[i]['d_a_date1'].month)
                            term['time'] = yyyy_mm
                            term[result_deposit[i]['b_name2']] = result_deposit[i]['d_a_money1']
                            rawData.append(term)

                        else:
                            if result_deposit[i]['b_name2'] not in rawData[loc]:
                                #rawdata中有这一年  但是没有这条记录所在的支行  添加支行
                                rawData[loc][result_deposit[i]['b_name2']] = result_deposit[i]['d_a_money1']
                            else:
                                rawData[loc][result_deposit[i]['b_name2']] += result_deposit[i]['d_a_money1']
                    
                    if  result_check or result_deposit :
                        response = make_response(
                            jsonify(
                                {
                                    'code': 200,
                                    'columnList':columnList,
                                        'rawData': rawData
                                                                        
                                        
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
            #===============================以season为粒度=================================================================
                elif timegrain == 'season':
            
                    sqlcommand_check = ""
                    sqlcommand_check_term = ""
                    if (len(lowerBound) > 0) :
                        sqlcommand_check_term = sqlcommand_check_term + "  CHECK_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                    if (len(upperBound) > 0) :
                        sqlcommand_check_term = sqlcommand_check_term + " AND CHECK_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                    
                    sqlcommand_check = sqlcommand_check + '''
                    
                        SELECT 	CUSTOMER_CHECK_ACCOUNT.BANK_NAME AS B_name1,                                  
                                NEW_CHECK_ACCOUNT.C_A_money AS C_A_money1,
                                NEW_CHECK_ACCOUNT.C_A_date AS C_A_date1

                        FROM( 
                                SELECT 
                                    CHECK_ACCOUNT_ID AS C_A_ID, 
                                    CHECK_ACCOUNT_MONEY AS C_A_money,
                                    CHECK_ACCOUNT_REGDATE AS  C_A_date
                                FROM CHECK_ACCOUNT 
                                WHERE ''' + sqlcommand_check_term + '''
                                )NEW_CHECK_ACCOUNT,
                        
                                CUSTOMER_CHECK_ACCOUNT 
                        WHERE NEW_CHECK_ACCOUNT.C_A_ID = CUSTOMER_CHECK_ACCOUNT.CHECK_ACCOUNT_ID
                        ORDER BY NEW_CHECK_ACCOUNT.C_A_date ASC
      
                    '''
                    print(sqlcommand_check)
                    cursor.execute(sqlcommand_check)
                    cursor.rowfactory = makeDictFactory(cursor)
                    result_check = cursor.fetchall()
                    
                    print(result_check)

                    columnList = []
                    rawData = []

                    for i in range(len(result_check)):
                        if result_check[i]['b_name1'] not in columnList:
                            columnList.append(result_check[i]['b_name1'])
                    
                    for i in range(len(result_check)):
                        loc = locate_season(result_check[i]['c_a_date1'].year,result_check[i]['c_a_date1'].month, rawData)
                        if  loc == -1 :
                            #如果这是 rawdata中没有的 season
                            term = {}
                            s = math.ceil(result_check[i]['c_a_date1'].month/3)
                            season = str(result_check[i]['c_a_date1'].year) + '-' + str(s) 
                            term['time'] = season
                            term[result_check[i]['b_name1']] = result_check[i]['c_a_money1']
                            rawData.append(term)

                        else:
                            if result_check[i]['b_name1'] not in rawData[loc]:
                                #rawdata中有这一年  但是没有这条记录所在的支行  添加支行
                                rawData[loc][result_check[i]['b_name1']] = result_check[i]['c_a_money1']
                            else:
                                rawData[loc][result_check[i]['b_name1']] += result_check[i]['c_a_money1']
                    
                    

                    #----------deposit account--------

                    sqlcommand_deposit = ""
                    sqlcommand_deposit_term = ""
                    if (len(lowerBound) > 0) :
                        sqlcommand_deposit_term = sqlcommand_deposit_term + "  DEPOSIT_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                    if (len(upperBound) > 0) :
                        sqlcommand_deposit_term = sqlcommand_deposit_term + " AND DEPOSIT_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                    
                    sqlcommand_deposit = sqlcommand_deposit + '''
                    
                        SELECT 	CUSTOMER_DEPOSIT_ACCOUNT.BANK_NAME AS B_name2,                                  
                                NEW_DEPOSIT_ACCOUNT.D_A_money AS D_A_money1,
                                NEW_DEPOSIT_ACCOUNT.D_A_date AS D_A_date1

                        FROM( 
                                SELECT 
                                    DEPOSIT_ACCOUNT_ID AS D_A_ID, 
                                    DEPOSIT_ACCOUNT_MONEY AS D_A_money,
                                    DEPOSIT_ACCOUNT_REGDATE AS  D_A_date
                                FROM DEPOSIT_ACCOUNT 
                                WHERE ''' + sqlcommand_deposit_term + '''
                                )NEW_DEPOSIT_ACCOUNT,
                        
                                CUSTOMER_DEPOSIT_ACCOUNT 
                        WHERE NEW_DEPOSIT_ACCOUNT.D_A_ID = CUSTOMER_DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_ID
                        ORDER BY NEW_DEPOSIT_ACCOUNT.D_A_date ASC
      
                    '''
                    print(sqlcommand_deposit)
                    cursor.execute(sqlcommand_deposit)
                    cursor.rowfactory = makeDictFactory(cursor)
                    result_deposit = cursor.fetchall()
                    
                    print(result_deposit)

                    for i in range(len(result_deposit)):
                        if result_deposit[i]['b_name2'] not in columnList:
                            columnList.append(result_deposit[i]['b_name2'])
                    
                    for i in range(len(result_deposit)):
                        loc = locate_season(result_deposit[i]['d_a_date1'].year, result_deposit[i]['d_a_date1'].month, rawData)
                        if  loc == -1 :
                            #如果这是 rawdata中没有的 year-season
                            term = {}
                            s = math.ceil(result_deposit[i]['d_a_date1'].month/3)
                            season = str(result_deposit[i]['d_a_date1'].year) + '-' + str(s)
                            term['time'] = season
                            term[result_deposit[i]['b_name2']] = result_deposit[i]['d_a_money1']
                            rawData.append(term)

                        else:
                            if result_deposit[i]['b_name2'] not in rawData[loc]:
                                #rawdata中有这season  但是没有这条记录所在的支行  添加支行
                                rawData[loc][result_deposit[i]['b_name2']] = result_deposit[i]['d_a_money1']
                            else:
                                rawData[loc][result_deposit[i]['b_name2']] += result_deposit[i]['d_a_money1']
                    
                    if  result_check or result_deposit :
                        response = make_response(
                            jsonify(
                                {
                                    'code': 200,
                                    'columnList':columnList,
                                        'rawData': rawData
                                                                        
                                        
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

            if sumtype == 'loan':
        #===============================贷款业务=================================================================
        #===============================以年为粒度=================================================================    
                if timegrain == 'year':        
                    
                    sqlcommand_loan = ""
                    sqlcommand_loan_term = ""
                    if (len(lowerBound) > 0) :
                        sqlcommand_loan_term = sqlcommand_loan_term + " PAY_DATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                    if (len(upperBound) > 0) :
                        sqlcommand_loan_term = sqlcommand_loan_term + " AND PAY_DATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                    
                    sqlcommand_loan = sqlcommand_loan + '''
                    
                    
                        SELECT 	NEW_PAY.loan_id0 AS loan_id1, 
                                NEW_PAY.pay_date0 AS pay_date1, 
                                NEW_PAY.pay_money0 AS pay_money1,
                                LOAN.BANK_NAME AS bank_name1 
                        FROM( 
                                SELECT 
                                    LOAN_ID AS loan_id0, 
                                    PAY_DATE AS pay_date0, 
                                    PAY_MONEY AS pay_money0
                                FROM PAY 
                                WHERE ''' + sqlcommand_loan_term + '''
                            )NEW_PAY, LOAN

                        WHERE NEW_PAY.loan_id0 = LOAN.LOAN_ID
                        
                    '''
                    print(sqlcommand_loan)
                    cursor.execute(sqlcommand_loan)
                    cursor.rowfactory = makeDictFactory(cursor)
                    result_loan = cursor.fetchall()
                    
                    print(result_loan)
                    #--------结果处理---------
                    columnList = []
                    rawData = []

                    for i in range(len(result_loan)):
                        if result_loan[i]['bank_name1'] not in columnList:
                            columnList.append(result_loan[i]['bank_name1'])
                    
                    for i in range(len(result_loan)):
                        loc = locate(result_loan[i]['pay_date1'].year, rawData)
                        if  loc == -1 :
                            #如果这是 rawdata中没有的 year
                            term = {}
                            term['time'] = str(result_loan[i]['pay_date1'].year)
                            term[result_loan[i]['bank_name1']] = result_loan[i]['pay_money1']
                            rawData.append(term)

                        else:
                            if result_loan[i]['bank_name1'] not in rawData[loc]:
                                #rawdata中有这一年  但是没有这条记录所在的支行  添加支行
                                rawData[loc][result_loan[i]['bank_name1']] = result_loan[i]['pay_money1']
                            else:
                                rawData[loc][result_loan[i]['bank_name1']] += result_loan[i]['pay_money1']
                    
                    if  result_loan  :
                        response = make_response(
                            jsonify(
                                {
                                    'code': 200,
                                    'columnList':columnList,
                                        'rawData': rawData
                                                                        
                                        
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

            #===============================以month为粒度=================================================================
                elif timegrain == 'month':            
                    
                    sqlcommand_loan = ""
                    sqlcommand_loan_term = ""
                    if (len(lowerBound) > 0) :
                        sqlcommand_loan_term = sqlcommand_loan_term + " PAY_DATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                    if (len(upperBound) > 0) :
                        sqlcommand_loan_term = sqlcommand_loan_term + " AND PAY_DATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                    
                    sqlcommand_loan = sqlcommand_loan + '''
                    
                    
                        SELECT 	NEW_PAY.loan_id0 AS loan_id1, 
                                NEW_PAY.pay_date0 AS pay_date1, 
                                NEW_PAY.pay_money0 AS pay_money1,
                                LOAN.BANK_NAME AS bank_name1 
                        FROM( 
                                SELECT 
                                    LOAN_ID AS loan_id0, 
                                    PAY_DATE AS pay_date0, 
                                    PAY_MONEY AS pay_money0
                                FROM PAY 
                                WHERE ''' + sqlcommand_loan_term + '''
                            )NEW_PAY, LOAN

                        WHERE NEW_PAY.loan_id0 = LOAN.LOAN_ID
                        
                    '''
                    print(sqlcommand_loan)
                    cursor.execute(sqlcommand_loan)
                    cursor.rowfactory = makeDictFactory(cursor)
                    result_loan = cursor.fetchall()
                    
                    print(result_loan)

                    #--------结果处理---------
                    columnList = []
                    rawData = []

                    for i in range(len(result_loan)):
                        if result_loan[i]['bank_name1'] not in columnList:
                            columnList.append(result_loan[i]['bank_name1'])
                    
                    for i in range(len(result_loan)):
                        loc = locate_month(result_loan[i]['pay_date1'].year,result_loan[i]['pay_date1'].month, rawData)
                        if  loc == -1 :
                            #如果这是 rawdata中没有的 m
                            term = {}
                            term['time'] = str(result_loan[i]['pay_date1'].year) + '.' + str(result_loan[i]['pay_date1'].month)
                            term[result_loan[i]['bank_name1']] = result_loan[i]['pay_money1']
                            rawData.append(term)

                        else:
                            if result_loan[i]['bank_name1'] not in rawData[loc]:
                                #rawdata中有这一m  但是没有这条记录所在的支行  添加支行
                                rawData[loc][result_loan[i]['bank_name1']] = result_loan[i]['pay_money1']
                            else:
                                rawData[loc][result_loan[i]['bank_name1']] += result_loan[i]['pay_money1']
                    
                    if  result_loan  :
                        response = make_response(
                            jsonify(
                                {
                                    'code': 200,
                                    'columnList':columnList,
                                        'rawData': rawData
                                                                        
                                        
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

            #===============================以season为粒度=================================================================
                elif timegrain == 'season':            
                    
                    sqlcommand_loan = ""
                    sqlcommand_loan_term = ""
                    if (len(lowerBound) > 0) :
                        sqlcommand_loan_term = sqlcommand_loan_term + " PAY_DATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                    if (len(upperBound) > 0) :
                        sqlcommand_loan_term = sqlcommand_loan_term + " AND PAY_DATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                    
                    sqlcommand_loan = sqlcommand_loan + '''
                    
                    
                        SELECT 	NEW_PAY.loan_id0 AS loan_id1, 
                                NEW_PAY.pay_date0 AS pay_date1, 
                                NEW_PAY.pay_money0 AS pay_money1,
                                LOAN.BANK_NAME AS bank_name1 
                        FROM( 
                                SELECT 
                                    LOAN_ID AS loan_id0, 
                                    PAY_DATE AS pay_date0, 
                                    PAY_MONEY AS pay_money0
                                FROM PAY 
                                WHERE ''' + sqlcommand_loan_term + '''
                            )NEW_PAY, LOAN

                        WHERE NEW_PAY.loan_id0 = LOAN.LOAN_ID
                        
                    '''
                    print(sqlcommand_loan)
                    cursor.execute(sqlcommand_loan)
                    cursor.rowfactory = makeDictFactory(cursor)
                    result_loan = cursor.fetchall()
                    
                    print(result_loan)
                    #--------结果处理---------
                    columnList = []
                    rawData = []

                    for i in range(len(result_loan)):
                        if result_loan[i]['bank_name1'] not in columnList:
                            columnList.append(result_loan[i]['bank_name1'])
                    
                    for i in range(len(result_loan)):
                        loc = locate_season(result_loan[i]['pay_date1'].year,result_loan[i]['pay_date1'].month, rawData)
                        if  loc == -1 :
                            #如果这是 rawdata中没有的 m
                            s = math.ceil(result_loan[i]['pay_date1'].month/3)
                            term = {}
                            term['time'] = str(result_loan[i]['pay_date1'].year) + '-' + str(s)
                            term[result_loan[i]['bank_name1']] = result_loan[i]['pay_money1']
                            rawData.append(term)

                        else:
                            if result_loan[i]['bank_name1'] not in rawData[loc]:
                                #rawdata中有这一m  但是没有这条记录所在的支行  添加支行
                                rawData[loc][result_loan[i]['bank_name1']] = result_loan[i]['pay_money1']
                            else:
                                rawData[loc][result_loan[i]['bank_name1']] += result_loan[i]['pay_money1']
                    
                    if  result_loan  :
                        response = make_response(
                            jsonify(
                                {
                                    'code': 200,
                                    'columnList':columnList,
                                        'rawData': rawData
                                                                        
                                        
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

    #=======================================用户统计======================================================================
        if datatype == 'user':

            #===================================存储业务==================================================================
            if sumtype == 'saving':
                #===============================以年为粒度=====================================================================
                if timegrain == 'year':#---
                    #-------check-----account-----
                    sqlcommand_check = ""
                    sqlcommand_check_term = ""
                    if (len(lowerBound) > 0) :
                        sqlcommand_check_term = sqlcommand_check_term + "  CHECK_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                    if (len(upperBound) > 0) :
                        sqlcommand_check_term = sqlcommand_check_term + " AND CHECK_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                    
                    sqlcommand_check = sqlcommand_check + '''
                    
                    
                        SELECT 	CUSTOMER_CHECK_ACCOUNT.BANK_NAME AS B_name1, 
                                NEW_CHECK_ACCOUNT.C_A_date0 AS c_a_date1,
                                CUSTOMER_CHECK_ACCOUNT.CUSTOMER_ID AS customer_id1
                                
                                                        
                        FROM( 
                                SELECT 
                                    CHECK_ACCOUNT_ID AS C_A_ID0,
                                    CHECK_ACCOUNT_REGDATE AS  C_A_date0

                                FROM CHECK_ACCOUNT 
                                WHERE ''' + sqlcommand_check_term + '''
                                )NEW_CHECK_ACCOUNT,  CUSTOMER_CHECK_ACCOUNT 

                        WHERE NEW_CHECK_ACCOUNT.C_A_ID0 = CUSTOMER_CHECK_ACCOUNT.CHECK_ACCOUNT_ID
                  
                    '''
                    print(sqlcommand_check)
                    cursor.execute(sqlcommand_check)
                    cursor.rowfactory = makeDictFactory(cursor)
                    result_check = cursor.fetchall()
                    
                    print(result_check)

                    columnList = []
                    rawData = []

                    for i in range(len(result_check)):
                        if result_check[i]['b_name1'] not in columnList:
                            columnList.append(result_check[i]['b_name1'])
                    
                    for i in range(len(result_check)):
                        loc = locate(result_check[i]['c_a_date1'].year, rawData)
                        if  loc == -1 :
                            #如果这是 rawdata中没有的 一年
                            term = {}
                            term['time'] = str(result_check[i]['c_a_date1'].year)
                            term[result_check[i]['b_name1']] = []
                            term[result_check[i]['b_name1']].append(result_check[i]['customer_id1']) 
                            rawData.append(term)

                        else:
                            if result_check[i]['b_name1'] not in rawData[loc]:
                                #rawdata中有这一年  但是没有这条记录所在的支行  添加支行
                                rawData[loc][result_check[i]['b_name1']] = []
                                #将新用户添加到XX支行的列表中
                                rawData[loc][result_check[i]['b_name1']].append(result_check[i]['customer_id1'])
                            else:
                                if result_check[i]['customer_id1'] not in rawData[loc][result_check[i]['b_name1']]:
                                    rawData[loc][result_check[i]['b_name1']].append(result_check[i]['customer_id1'])
 
                    #----------deposit account--------

                    sqlcommand_deposit = ""
                    sqlcommand_deposit_term = ""
                    if (len(lowerBound) > 0) :
                        sqlcommand_deposit_term = sqlcommand_deposit_term + "  DEPOSIT_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                    if (len(upperBound) > 0) :
                        sqlcommand_deposit_term = sqlcommand_deposit_term + " AND DEPOSIT_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                    
                    sqlcommand_deposit = sqlcommand_deposit + '''

                     
                        SELECT 	CUSTOMER_DEPOSIT_ACCOUNT.BANK_NAME AS B_name2, 
                                
                                NEW_DEPOSIT_ACCOUNT.d_a_date0 AS d_a_date1,
                                CUSTOMER_DEPOSIT_ACCOUNT.CUSTOMER_ID AS customer_id2
                        FROM( 
                                SELECT 
                                    DEPOSIT_ACCOUNT_ID AS D_A_ID0,
                                    DEPOSIT_ACCOUNT_REGDATE AS d_a_date0
                                FROM DEPOSIT_ACCOUNT 
                                WHERE '''+ sqlcommand_deposit_term +'''

                                )NEW_DEPOSIT_ACCOUNT,CUSTOMER_DEPOSIT_ACCOUNT

                        WHERE NEW_DEPOSIT_ACCOUNT.D_A_ID0 = CUSTOMER_DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_ID
                        
                '''
                    print(sqlcommand_deposit)
                    cursor.execute(sqlcommand_deposit)
                    cursor.rowfactory = makeDictFactory(cursor)
                    result_deposit = cursor.fetchall()
                    
                    print(result_deposit)

                    #=============用户统计==存储业务===年为粒度===结果处理======
                    for i in range(len(result_deposit)):
                        if result_deposit[i]['b_name2'] not in columnList:
                            columnList.append(result_deposit[i]['b_name2'])
                    
                    for i in range(len(result_deposit)):
                        loc = locate(result_deposit[i]['d_a_date1'].year, rawData)
                        if  loc == -1 :
                            #如果这是 rawdata中没有的 一年
                            term = {}
                            term['time'] = str(result_deposit[i]['d_a_date1'].year)
                            term[result_deposit[i]['b_name2']] = []
                            term[result_deposit[i]['b_name2']].append(result_deposit[i]['customer_id2'])
                            
                            rawData.append(term)

                        else:
                            if result_deposit[i]['b_name2'] not in rawData[loc]:
                                #rawdata中有这一年  但是没有这条记录所在的支行  添加支行
                                rawData[loc][result_deposit[i]['b_name2']] = []
                                #将新用户添加到XX支行的列表中
                                rawData[loc][result_deposit[i]['b_name2']].append(result_deposit[i]['customer_id2'])
                            else:
                                if result_deposit[i]['customer_id2'] not in rawData[loc][result_deposit[i]['b_name2']]:
                                    rawData[loc][result_deposit[i]['b_name2']].append(result_deposit[i]['customer_id2'])
                   
                    for i in range(len(rawData)):
                        for key in rawData[i]:
                            if key != 'time':

                                if len(rawData[i][key])>0:
                                    rawData[i][key] = len(rawData[i][key])

                    if  result_check or result_deposit :
                        response = make_response(
                            jsonify(
                                {
                                    'code': 200,
                                    'columnList':columnList,
                                        'rawData': rawData
                                                                        
                                        
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

                #===============================以month为粒度=====================================================================
                elif timegrain == 'month':#---
                    #-------check-----account-----
                    sqlcommand_check = ""
                    sqlcommand_check_term = ""
                    if (len(lowerBound) > 0) :
                        sqlcommand_check_term = sqlcommand_check_term + "  CHECK_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                    if (len(upperBound) > 0) :
                        sqlcommand_check_term = sqlcommand_check_term + " AND CHECK_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                    
                    sqlcommand_check = sqlcommand_check + '''
                    
                    
                        SELECT 	CUSTOMER_CHECK_ACCOUNT.BANK_NAME AS B_name1, 
                                NEW_CHECK_ACCOUNT.C_A_date0 AS c_a_date1,
                                CUSTOMER_CHECK_ACCOUNT.CUSTOMER_ID AS customer_id1
                                
                                                        
                        FROM( 
                                SELECT 
                                    CHECK_ACCOUNT_ID AS C_A_ID0,
                                    CHECK_ACCOUNT_REGDATE AS  C_A_date0

                                FROM CHECK_ACCOUNT 
                                WHERE ''' + sqlcommand_check_term + '''
                                )NEW_CHECK_ACCOUNT,  CUSTOMER_CHECK_ACCOUNT 

                        WHERE NEW_CHECK_ACCOUNT.C_A_ID0 = CUSTOMER_CHECK_ACCOUNT.CHECK_ACCOUNT_ID
                  
                    '''
                    print(sqlcommand_check)
                    cursor.execute(sqlcommand_check)
                    cursor.rowfactory = makeDictFactory(cursor)
                    result_check = cursor.fetchall()
                    
                    print(result_check)

                    columnList = []
                    rawData = []

                    for i in range(len(result_check)):
                        if result_check[i]['b_name1'] not in columnList:
                            columnList.append(result_check[i]['b_name1'])
                    
                    for i in range(len(result_check)):
                        loc = locate_month(result_check[i]['c_a_date1'].year,result_check[i]['c_a_date1'].month, rawData)
                        if  loc == -1 :
                            #如果这是 rawdata中没有的 一月
                            term = {}
                            term['time'] = str(result_check[i]['c_a_date1'].year) + '.' + str(result_check[i]['c_a_date1'].month)
                            term[result_check[i]['b_name1']] = []
                            term[result_check[i]['b_name1']].append(result_check[i]['customer_id1']) 
                            rawData.append(term)

                        else:
                            if result_check[i]['b_name1'] not in rawData[loc]:
                                #rawdata中有这一月  但是没有这条记录所在的支行  添加支行
                                rawData[loc][result_check[i]['b_name1']] = []
                                #将新用户添加到XX支行的列表中
                                rawData[loc][result_check[i]['b_name1']].append(result_check[i]['customer_id1'])
                            else:
                                if result_check[i]['customer_id1'] not in rawData[loc][result_check[i]['b_name1']]:
                                    rawData[loc][result_check[i]['b_name1']].append(result_check[i]['customer_id1'])
 
                    #----------deposit account--------

                    sqlcommand_deposit = ""
                    sqlcommand_deposit_term = ""
                    if (len(lowerBound) > 0) :
                        sqlcommand_deposit_term = sqlcommand_deposit_term + "  DEPOSIT_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                    if (len(upperBound) > 0) :
                        sqlcommand_deposit_term = sqlcommand_deposit_term + " AND DEPOSIT_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                    
                    sqlcommand_deposit = sqlcommand_deposit + '''

                     
                        SELECT 	CUSTOMER_DEPOSIT_ACCOUNT.BANK_NAME AS B_name2, 
                                
                                NEW_DEPOSIT_ACCOUNT.d_a_date0 AS d_a_date1,
                                CUSTOMER_DEPOSIT_ACCOUNT.CUSTOMER_ID AS customer_id2
                        FROM( 
                                SELECT 
                                    DEPOSIT_ACCOUNT_ID AS D_A_ID0,
                                    DEPOSIT_ACCOUNT_REGDATE AS d_a_date0
                                FROM DEPOSIT_ACCOUNT 
                                WHERE '''+ sqlcommand_deposit_term +'''

                                )NEW_DEPOSIT_ACCOUNT,CUSTOMER_DEPOSIT_ACCOUNT

                        WHERE NEW_DEPOSIT_ACCOUNT.D_A_ID0 = CUSTOMER_DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_ID
                        
                '''
                    print(sqlcommand_deposit)
                    cursor.execute(sqlcommand_deposit)
                    cursor.rowfactory = makeDictFactory(cursor)
                    result_deposit = cursor.fetchall()
                    
                    print(result_deposit)

                    #=============用户统计==存储业务===年为粒度===结果处理======
                    for i in range(len(result_deposit)):
                        if result_deposit[i]['b_name2'] not in columnList:
                            columnList.append(result_deposit[i]['b_name2'])
                    
                    for i in range(len(result_deposit)):
                        loc = locate_month(result_deposit[i]['d_a_date1'].year, result_deposit[i]['d_a_date1'].month,rawData)
                        if  loc == -1 :
                            #如果这是 rawdata中没有的 一年
                            term = {}
                            term['time'] = str(result_deposit[i]['d_a_date1'].year) + '.' + str(result_deposit[i]['d_a_date1'].month)
                            term[result_deposit[i]['b_name2']] = []
                            term[result_deposit[i]['b_name2']].append(result_deposit[i]['customer_id2'])
                            
                            rawData.append(term)

                        else:
                            if result_deposit[i]['b_name2'] not in rawData[loc]:
                                #rawdata中有这一年  但是没有这条记录所在的支行  添加支行
                                rawData[loc][result_deposit[i]['b_name2']] = []
                                #将新用户添加到XX支行的列表中
                                rawData[loc][result_deposit[i]['b_name2']].append(result_deposit[i]['customer_id2'])
                            else:
                                if result_deposit[i]['customer_id2'] not in rawData[loc][result_deposit[i]['b_name2']]:
                                    rawData[loc][result_deposit[i]['b_name2']].append(result_deposit[i]['customer_id2'])
                   
                    for i in range(len(rawData)):
                        for key in rawData[i]:
                            if key != 'time':

                                if len(rawData[i][key])>0:
                                    rawData[i][key] = len(rawData[i][key])

                    if  result_check or result_deposit :
                        response = make_response(
                            jsonify(
                                {
                                    'code': 200,
                                    'columnList':columnList,
                                        'rawData': rawData
                                                                        
                                        
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
            #===============================以season为粒度=====================================================================
                elif timegrain == 'season':#---
                    #-------check-----account-----
                    sqlcommand_check = ""
                    sqlcommand_check_term = ""
                    if (len(lowerBound) > 0) :
                        sqlcommand_check_term = sqlcommand_check_term + "  CHECK_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                    if (len(upperBound) > 0) :
                        sqlcommand_check_term = sqlcommand_check_term + " AND CHECK_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                    
                    sqlcommand_check = sqlcommand_check + '''
                    
                    
                        SELECT 	CUSTOMER_CHECK_ACCOUNT.BANK_NAME AS B_name1, 
                                NEW_CHECK_ACCOUNT.C_A_date0 AS c_a_date1,
                                CUSTOMER_CHECK_ACCOUNT.CUSTOMER_ID AS customer_id1
                                
                                                        
                        FROM( 
                                SELECT 
                                    CHECK_ACCOUNT_ID AS C_A_ID0,
                                    CHECK_ACCOUNT_REGDATE AS  C_A_date0

                                FROM CHECK_ACCOUNT 
                                WHERE ''' + sqlcommand_check_term + '''
                                )NEW_CHECK_ACCOUNT,  CUSTOMER_CHECK_ACCOUNT 

                        WHERE NEW_CHECK_ACCOUNT.C_A_ID0 = CUSTOMER_CHECK_ACCOUNT.CHECK_ACCOUNT_ID
                  
                    '''
                    print(sqlcommand_check)
                    cursor.execute(sqlcommand_check)
                    cursor.rowfactory = makeDictFactory(cursor)
                    result_check = cursor.fetchall()
                    
                    print(result_check)

                    columnList = []
                    rawData = []

                    for i in range(len(result_check)):
                        if result_check[i]['b_name1'] not in columnList:
                            columnList.append(result_check[i]['b_name1'])
                    
                    for i in range(len(result_check)):
                        loc = locate_season(result_check[i]['c_a_date1'].year,result_check[i]['c_a_date1'].month, rawData)
                        if  loc == -1 :
                            #如果这是 rawdata中没有的 一season
                            term = {}
                            s = math.ceil(result_check[i]['c_a_date1'].month/3)
                            term['time'] = str(result_check[i]['c_a_date1'].year) + '-' + str(s)
                            term[result_check[i]['b_name1']] = []
                            term[result_check[i]['b_name1']].append(result_check[i]['customer_id1']) 
                            rawData.append(term)

                        else:
                            if result_check[i]['b_name1'] not in rawData[loc]:
                                #rawdata中有这一月  但是没有这条记录所在的支行  添加支行
                                rawData[loc][result_check[i]['b_name1']] = []
                                #将新用户添加到XX支行的列表中
                                rawData[loc][result_check[i]['b_name1']].append(result_check[i]['customer_id1'])
                            else:
                                if result_check[i]['customer_id1'] not in rawData[loc][result_check[i]['b_name1']]:
                                    rawData[loc][result_check[i]['b_name1']].append(result_check[i]['customer_id1'])
 
                    #----------deposit account--------

                    sqlcommand_deposit = ""
                    sqlcommand_deposit_term = ""
                    if (len(lowerBound) > 0) :
                        sqlcommand_deposit_term = sqlcommand_deposit_term + "  DEPOSIT_ACCOUNT_REGDATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                    if (len(upperBound) > 0) :
                        sqlcommand_deposit_term = sqlcommand_deposit_term + " AND DEPOSIT_ACCOUNT_REGDATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                    
                    sqlcommand_deposit = sqlcommand_deposit + '''

                     
                        SELECT 	CUSTOMER_DEPOSIT_ACCOUNT.BANK_NAME AS B_name2, 
                                
                                NEW_DEPOSIT_ACCOUNT.d_a_date0 AS d_a_date1,
                                CUSTOMER_DEPOSIT_ACCOUNT.CUSTOMER_ID AS customer_id2
                        FROM( 
                                SELECT 
                                    DEPOSIT_ACCOUNT_ID AS D_A_ID0,
                                    DEPOSIT_ACCOUNT_REGDATE AS d_a_date0
                                FROM DEPOSIT_ACCOUNT 
                                WHERE '''+ sqlcommand_deposit_term +'''

                                )NEW_DEPOSIT_ACCOUNT,CUSTOMER_DEPOSIT_ACCOUNT

                        WHERE NEW_DEPOSIT_ACCOUNT.D_A_ID0 = CUSTOMER_DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_ID
                        
                '''
                    print(sqlcommand_deposit)
                    cursor.execute(sqlcommand_deposit)
                    cursor.rowfactory = makeDictFactory(cursor)
                    result_deposit = cursor.fetchall()
                    
                    print(result_deposit)

                    #=============用户统计==存储业务===年为粒度===结果处理======
                    for i in range(len(result_deposit)):
                        if result_deposit[i]['b_name2'] not in columnList:
                            columnList.append(result_deposit[i]['b_name2'])
                    
                    for i in range(len(result_deposit)):
                        loc = locate_season(result_deposit[i]['d_a_date1'].year, result_deposit[i]['d_a_date1'].month,rawData)
                        if  loc == -1 :
                            #如果这是 rawdata中没有的 一年
                            term = {}
                            s = math.ceil(result_deposit[i]['d_a_date1'].month/3)
                            term['time'] = str(result_deposit[i]['d_a_date1'].year) + '-' + str(s)
                            term[result_deposit[i]['b_name2']] = []
                            term[result_deposit[i]['b_name2']].append(result_deposit[i]['customer_id2'])
                            
                            rawData.append(term)

                        else:
                            if result_deposit[i]['b_name2'] not in rawData[loc]:
                                #rawdata中有这一年  但是没有这条记录所在的支行  添加支行
                                rawData[loc][result_deposit[i]['b_name2']] = []
                                #将新用户添加到XX支行的列表中
                                rawData[loc][result_deposit[i]['b_name2']].append(result_deposit[i]['customer_id2'])
                            else:
                                if result_deposit[i]['customer_id2'] not in rawData[loc][result_deposit[i]['b_name2']]:
                                    rawData[loc][result_deposit[i]['b_name2']].append(result_deposit[i]['customer_id2'])
                   
                    for i in range(len(rawData)):
                        for key in rawData[i]:
                            if key != 'time':

                                if len(rawData[i][key])>0:
                                    rawData[i][key] = len(rawData[i][key])

                    if  result_check or result_deposit :
                        response = make_response(
                            jsonify(
                                {
                                    'code': 200,
                                    'columnList':columnList,
                                        'rawData': rawData
                                                                        
                                        
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

            #===================================贷款业务==================================================================
            elif sumtype == 'loan':     
                #===============================以年为粒度=====================================================================
                if timegrain == 'year':#---
                                 
                    sqlcommand_loan = ""
                    sqlcommand_loan_term = ""
                    if (len(lowerBound) > 0) :
                        sqlcommand_loan_term = sqlcommand_loan_term + " PAY_DATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                    if (len(upperBound) > 0) :
                        sqlcommand_loan_term = sqlcommand_loan_term + " AND PAY_DATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                    
                    sqlcommand_loan = sqlcommand_loan + '''
                    
                    
                        SELECT 	
                                
                                LOAN.BANK_NAME AS b_name3,
                                LOAN_CUSTOMER.CUSTOMER_ID AS customer_id3,
                                NEW_PAY.pay_date0 AS pay_date3 
                        FROM( 
                                SELECT 
                                    LOAN_ID AS loan_id0,
                                    PAY_DATE AS pay_date0

                                FROM PAY 
                                WHERE ''' + sqlcommand_loan_term + '''
                            )NEW_PAY, LOAN, LOAN_CUSTOMER

                        WHERE NEW_PAY.loan_id0 = LOAN.LOAN_ID and NEW_PAY.loan_id0 = LOAN_CUSTOMER.LOAN_ID
                        
                        
                    '''
                    print(sqlcommand_loan)
                    cursor.execute(sqlcommand_loan)
                    cursor.rowfactory = makeDictFactory(cursor)
                    result_loan = cursor.fetchall()
                    
                    print(result_loan)

                    #-------用户统计----贷款业务-------结果处理---------

                    columnList = []
                    rawData = []

                    for i in range(len(result_loan)):
                        if result_loan[i]['b_name3'] not in columnList:
                            columnList.append(result_loan[i]['b_name3'])
                    
                    for i in range(len(result_loan)):
                        loc = locate(result_loan[i]['pay_date3'].year, rawData)
                        if  loc == -1 :
                            #如果这是 rawdata中没有的 一年
                            term = {}
                            term['time'] = str(result_loan[i]['pay_date3'].year)
                            term[result_loan[i]['b_name3']] = []
                            term[result_loan[i]['b_name3']].append(result_loan[i]['customer_id3'])
                            
                            rawData.append(term)

                        else:
                            if result_loan[i]['b_name3'] not in rawData[loc]:
                                #rawdata中有这一年  但是没有这条记录所在的支行  添加支行
                                rawData[loc][result_loan[i]['b_name3']] = []
                                #将新用户添加到XX支行的列表中
                                rawData[loc][result_loan[i]['b_name3']].append(result_loan[i]['customer_id3'])
                            else:
                                if result_loan[i]['customer_id3'] not in rawData[loc][result_loan[i]['b_name3']]:
                                    rawData[loc][result_loan[i]['b_name3']].append(result_loan[i]['customer_id3'])
                   
                    for i in range(len(rawData)):
                        for key in rawData[i]:
                            if key != 'time':

                                if len(rawData[i][key])>0:
                                    rawData[i][key] = len(rawData[i][key])

                    if  result_loan :
                        response = make_response(
                            jsonify(
                                {
                                    'code': 200,
                                    'columnList':columnList,
                                        'rawData': rawData
                                                                        
                                        
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
                    
                #===============================以month为粒度=====================================================================
                elif timegrain == 'month':#---
                                 
                    sqlcommand_loan = ""
                    sqlcommand_loan_term = ""
                    if (len(lowerBound) > 0) :
                        sqlcommand_loan_term = sqlcommand_loan_term + " PAY_DATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                    if (len(upperBound) > 0) :
                        sqlcommand_loan_term = sqlcommand_loan_term + " AND PAY_DATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                    
                    sqlcommand_loan = sqlcommand_loan + '''
                    
                    
                        SELECT 	
                                
                                LOAN.BANK_NAME AS b_name3,
                                LOAN_CUSTOMER.CUSTOMER_ID AS customer_id3,
                                NEW_PAY.pay_date0 AS pay_date3 
                        FROM( 
                                SELECT 
                                    LOAN_ID AS loan_id0,
                                    PAY_DATE AS pay_date0

                                FROM PAY 
                                WHERE ''' + sqlcommand_loan_term + '''
                            )NEW_PAY, LOAN, LOAN_CUSTOMER

                        WHERE NEW_PAY.loan_id0 = LOAN.LOAN_ID and NEW_PAY.loan_id0 = LOAN_CUSTOMER.LOAN_ID
                        
                        
                    '''
                    print(sqlcommand_loan)
                    cursor.execute(sqlcommand_loan)
                    cursor.rowfactory = makeDictFactory(cursor)
                    result_loan = cursor.fetchall()
                    
                    print(result_loan)

                    #-------用户统计----贷款业务-------结果处理---------

                    columnList = []
                    rawData = []

                    for i in range(len(result_loan)):
                        if result_loan[i]['b_name3'] not in columnList:
                            columnList.append(result_loan[i]['b_name3'])
                    
                    for i in range(len(result_loan)):
                        loc = locate_month(result_loan[i]['pay_date3'].year,result_loan[i]['pay_date3'].month, rawData)
                        if  loc == -1 :
                            #如果这是 rawdata中没有的 一年
                            term = {}
                            term['time'] = str(result_loan[i]['pay_date3'].year)+'.'+str(result_loan[i]['pay_date3'].month)
                            term[result_loan[i]['b_name3']] = []
                            term[result_loan[i]['b_name3']].append(result_loan[i]['customer_id3'])
                            
                            rawData.append(term)

                        else:
                            if result_loan[i]['b_name3'] not in rawData[loc]:
                                #rawdata中有这一年  但是没有这条记录所在的支行  添加支行
                                rawData[loc][result_loan[i]['b_name3']] = []
                                #将新用户添加到XX支行的列表中
                                rawData[loc][result_loan[i]['b_name3']].append(result_loan[i]['customer_id3'])
                            else:
                                if result_loan[i]['customer_id3'] not in rawData[loc][result_loan[i]['b_name3']]:
                                    rawData[loc][result_loan[i]['b_name3']].append(result_loan[i]['customer_id3'])
                   
                    for i in range(len(rawData)):
                        for key in rawData[i]:
                            if key != 'time':

                                if len(rawData[i][key])>0:
                                    rawData[i][key] = len(rawData[i][key])

                    if  result_loan :
                        response = make_response(
                            jsonify(
                                {
                                    'code': 200,
                                    'columnList':columnList,
                                        'rawData': rawData
                                                                        
                                        
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

                #===============================以season为粒度=====================================================================
                elif timegrain == 'season':#---
                                 
                    sqlcommand_loan = ""
                    sqlcommand_loan_term = ""
                    if (len(lowerBound) > 0) :
                        sqlcommand_loan_term = sqlcommand_loan_term + " PAY_DATE > TO_DATE('" + lowerBound + "','YYYY-MM-DD')"
                    if (len(upperBound) > 0) :
                        sqlcommand_loan_term = sqlcommand_loan_term + " AND PAY_DATE < TO_DATE('" + upperBound + "','YYYY-MM-DD')"
                    
                    sqlcommand_loan = sqlcommand_loan + '''
                    
                    
                        SELECT 	
                                
                                LOAN.BANK_NAME AS b_name3,
                                LOAN_CUSTOMER.CUSTOMER_ID AS customer_id3,
                                NEW_PAY.pay_date0 AS pay_date3 
                        FROM( 
                                SELECT 
                                    LOAN_ID AS loan_id0,
                                    PAY_DATE AS pay_date0

                                FROM PAY 
                                WHERE ''' + sqlcommand_loan_term + '''
                            )NEW_PAY, LOAN, LOAN_CUSTOMER

                        WHERE NEW_PAY.loan_id0 = LOAN.LOAN_ID and NEW_PAY.loan_id0 = LOAN_CUSTOMER.LOAN_ID
                        
                        
                    '''
                    print(sqlcommand_loan)
                    cursor.execute(sqlcommand_loan)
                    cursor.rowfactory = makeDictFactory(cursor)
                    result_loan = cursor.fetchall()
                    
                    print(result_loan)

                    #-------用户统计----贷款业务-------结果处理---------

                    columnList = []
                    rawData = []

                    for i in range(len(result_loan)):
                        if result_loan[i]['b_name3'] not in columnList:
                            columnList.append(result_loan[i]['b_name3'])
                    
                    for i in range(len(result_loan)):
                        loc = locate_season(result_loan[i]['pay_date3'].year,result_loan[i]['pay_date3'].month, rawData)
                        if  loc == -1 :
                            #如果这是 rawdata中没有的 一年
                            term = {}
                            s = math.ceil(result_loan[i]['pay_date3'].month/3)
                            term['time'] = str(result_loan[i]['pay_date3'].year)+'-' + str(s)
                            term[result_loan[i]['b_name3']] = []
                            term[result_loan[i]['b_name3']].append(result_loan[i]['customer_id3'])
                            
                            rawData.append(term)

                        else:
                            if result_loan[i]['b_name3'] not in rawData[loc]:
                                #rawdata中有这一年  但是没有这条记录所在的支行  添加支行
                                rawData[loc][result_loan[i]['b_name3']] = []
                                #将新用户添加到XX支行的列表中
                                rawData[loc][result_loan[i]['b_name3']].append(result_loan[i]['customer_id3'])
                            else:
                                if result_loan[i]['customer_id3'] not in rawData[loc][result_loan[i]['b_name3']]:
                                    rawData[loc][result_loan[i]['b_name3']].append(result_loan[i]['customer_id3'])
                   
                    for i in range(len(rawData)):
                        for key in rawData[i]:
                            if key != 'time':

                                if len(rawData[i][key])>0:
                                    rawData[i][key] = len(rawData[i][key])

                    if  result_loan :
                        response = make_response(
                            jsonify(
                                {
                                    'code': 200,
                                    'columnList':columnList,
                                        'rawData': rawData
                                                                        
                                        
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
    

