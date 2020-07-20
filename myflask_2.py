import flask
import json
import requests
import urllib.parse
from  query_aql import *
from  query import *
from sqlalchemy import *
from threading import *
with open("config.json") as f:
    conf=json.load(f)


def database_connector():
    global conf
    connect_string = 'mysql+pymysql://'
    s = s + conf['user'] + ':' + conf['password'] + '@' + conf['host'] + '/' + conf['database']
    engine = create_engine(connect_string)
    return engine


def table_creator():
    engine = database_connector()
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
            Column('old_search_id', Integer, primary_key = True,nullable = False,autoincrement = True),
            Column('aql',String(255)),
            Column('mql', String(255)),
            Column('search_tag', String(255)),
            Column('is_fav_search',Boolean))
            meta.create_all(engine)
            return


def DataPreprocess(request):
    if request.method == 'POST':
        keys = request.form.keys()
        my_keys = ['old_search_id','aql','mql','search_tag','is_fav_search']
        decoded_values = dict()
        for k in my_keys:
            if k in keys:
                decoded_value = urllib.parse.unquote_plus(request.form[k])
                decoded_values[k] = decoded_value
            else:
                decoded_values[k] = None
        if(decoded_values['aql'] != None):
            myaql_query = aql_generate_query(decoded_value['aql'])
            decoded_values['aql'] = myaql_query
        if(decoded_values['mql'] != None):
            mysql_query = generate_query(decoded_value['sql']
            decoded_values['mql'] = mysql_query
        if(decoded_values['is_fav_search'] != None):
            if(decoded_values['is_fav_search'] == True):
                decoded_values['is_fav_search'] = 1
            else:
                decoded_values['is_fav_search'] = 0
        return decoded_values
    else:
        return "Invalid method"


def fetcher(decoded_values):
    queries_mql = dict()
    queries_aql = dict()
    column =''
    values =''
    for key in decoded_values.keys():
        if(decoded_values[key] != None and key != 'old_search_id')
            column = column + key + ','
            values = values + decoded_values[key] + ','
        elif(decoded_values[key] != None and key == 'old_search_id'):
            s ='select aql,mql from search_history where old_search_id = '
            s = s + decoded_values[key]
            queries_mql['old query'] = s 
        if(key == 'mql' and decoded_values[key] != None):
            queries_mql['new query'] = decoded_values[key]
        if(key == 'aql' and decoded_values[key] != None):
            queries_aql['new query'] = decoded_values[key]
    column = column.strip(',')
    values = values.strip(',')
    column = '(' + column + ')'
    values = '(' + values + ')'
    query = 'insert into search_history ' + column + 'values ' +values
    queries_mql['insert query'] = query
    engine = database_connector()
    for k in queries_mql.keys():
        if(k == 'insert query'):
            with engine.connect() as con:
                con.execute(queries_mql[k])
        elif(k == 'old query'):
            with engine.connect() as con:
                result = con.execute(queries_mql[k])
                for row in result:
                    if(row[0] != None):
                        queries_aql[k] = row[0]
                    if(row[1] != None):
                        queries_mql[k] = row[1]
    del queries_mql['insert query']
    return queries_mql,queries_aql

                         
def response(queries_mql,queries_aql):
    result = []
    engine = database_connector()
    for k in queries_mql.keys():
        with engine.connect() as con:
            temp_result = con.execute(queries_mql[k])
            temp_result = flask.jsonify({'result':temp_result}
            result.append(temp_result)
    '''
    aql query results
    '''
    return result


app = flask.Flask(__name__)
@app.route("/rest/search",methods=['POST'])
def hello():
    method = flask.method
    decoded_values = DataPreprocess(method)
    if(decoded_values == "Invalid method"):
        return decoded_values,400
    table_creator()
    queries_mql,queries_aql = fetcher(decoded_values)
    result = response(queries_mql,queries_aql)
    
if __name__ == "__main__": 
    app.run(host='0.0.0.0',debug = True)

