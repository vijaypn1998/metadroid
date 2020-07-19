import flask
import json
import requests
import query_aql
import urllib.parse
import query
from sqlalchemy import *
import pymysql
from sqlalchemy import *
with open("config.json") as f:
    conf=json.load(f)
def table_creator():
    global conf
    connect_string = 'mysql+pymysql://'
    s = s + conf['user'] + ':' + conf['password'] + '@' + conf['host'] + '/' + conf['database']
    engine = create_engine(connect_string)
    meta = MetaData()
    table_query ='''SELECT count(*)
    FROM information_schema.TABLES
    WHERE (TABLE_SCHEMA = 'database_1') AND (TABLE_NAME = 'huchu')'''
    with engine.connect() as con:
        result = con.execute(table_query)
        for row in result:
        if(row[0] == 1):
            return
        else:
            meta = MetaData()
            search_history = Table(
            'search_history', meta,
            Column('id', Integer, primary_key = True,nullable = False,autoincrement = True),
            Column('tag',String(255)),
            Column('aql_query', String(255)),
            Column('mql_query', String(255)),
            Column('fav',Boolean))
            meta.create_all(engine)
            return

app = flask.Flask(__name__)
@app.route("/rest/search",methods=['POST'])
def hello():
    if flask.request.method == 'POST':
        aql = flask.request.form['aql']
        mql = flask.request.form['mql']
        decoded_aql = urllib.parse.unquote_plus(aql)
        decoded_mql = urllib.parse.unquote_plus(mql)
        mysql_query=query.generate_query(decoded_mql)
        myaql_query = query_aql.aql_generate_query(decoded_aql)
        url='http://ambar/api/search?query='
        urls = []
        for query in myaql_query:
            a = url
            a = a + urllib.parse.quote(query)
            urls.append(a)
        try:
            mycursor.execute(mysql_query)
            myresult = mycursor.fetchall()
       
        except:
            return "Invalid MQL", 400
        url='http://ambar/api/search?query='
        urls = []
        responses = []
        for query in myaql_query:
            a = url
            a = a + urllib.parse.quote(query)
            urls.append(a)
        for u in urls:
            response = requests.get(u)
            data = response.json()
            responses.append(data)
    
        return flask.jsonify({"result":myresult})
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug = True)

