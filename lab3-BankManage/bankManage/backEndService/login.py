from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from flask_cors import *
import cx_Oracle

app = Flask(__name__)
CORS(app, supports_credentials=True)

def makeDictFactory(cursor):
    columnNames = [d[0].lower() for d in cursor.description]
    def createRow(*args):
        return dict(zip(columnNames, args))
    return createRow

@app.route('/')
def hello_world():
    return 'Hello Flask'

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    # print(username)
    # print(password)
    connection = cx_Oracle.connect('System/db2019@localhost/ORCL')
    cursor = connection.cursor()
    
    sqlcommand =    """
                    SELECT BANK_NAME AS username, BANK_PASS AS password 
                    FROM SUB_BANK
                    WHERE BANK_NAME = '""" + username + "'"
    print(sqlcommand)
    cursor.execute(sqlcommand)
    cursor.rowfactory = makeDictFactory(cursor)
    result = cursor.fetchone()
    print(result)

    cursor.close()
    connection.close()

    if result and result['password'][:len(password)] == password:
        response = make_response(jsonify({    
                                            'code':200,
                                            'msg':'get',
                                            'token':username
                                        })
                                    )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    response = make_response(jsonify({    
                                        'code':400,
                                        'msg':'error'
                                    })
                                )
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run()