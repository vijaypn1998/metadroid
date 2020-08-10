import flask
import json
import requests
import urllib.parse
from  query_aql import *
from  query import *
from sqlalchemy import *
from threading import *

result = []
with open("config.json") as f:
    conf=json.load(f)


def database_connector():
    global conf
    connect_string = 'mysql+pymysql://'
    connect_string = connect_string + conf['user'] + ':' + conf['password'] + '@' + conf['host'] + '/' + conf['database']
    engine = create_engine(connect_string)
    return engine


def table_creator():
    engine = database_connector()
    table_query ='''SELECT count(*)
    FROM information_schema.TABLES
    WHERE (TABLE_SCHEMA = 'database_1') AND (TABLE_NAME = 'search_history')'''
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
                Column('mql',String(255)),
                Column('aql', String(255)),
                Column('search_tag', String(255)),
                Column('is_fav_search',Boolean))
                meta.create_all(engine)
                return


def DataPreprocess(request):
    if request.method == 'POST':
        keys = request.form.keys()
        my_keys = ['old_search_id','aql','mql','search_tag','is_fav_search']
        keys_form = list(keys)
        decoded_values = {}
        for k in my_keys:
            if (k in keys_form):
                decoded_value = urllib.parse.unquote_plus(request.form[k])
                decoded_values[k] = decoded_value
            else:
                decoded_values[k] = None
        if(decoded_values['aql'] != None):
            try:
                myaql_query = aql_generate_query(decoded_values['aql'])
            except:
                return 'bad aql query'
            decoded_values['aql'] = myaql_query
        if(decoded_values['mql'] != None):
            try:
                mysql_query = generate_query(decoded_values['mql'])
            except:
                return 'bad sql query'
            decoded_values['mql'] = mysql_query
        if(decoded_values['is_fav_search'] != None):
            if(decoded_values['is_fav_search'] == 'True'):
                decoded_values['is_fav_search'] = 1
            else:
                decoded_values['is_fav_search'] = 0
        return decoded_values
    else:
        return 'Invalid Method'
    


def fetcher(decoded_values):
    queries_mql = dict()
    queries_aql = dict()
    column =''
    values =''
    for key in decoded_values.keys():
        if(key == 'aql' and decoded_values[key] != None):
            column = column + key + ','
            values = values +  "'" + decoded_values[key][0] + "'"  + ','
            queries_aql['new query'] = decoded_values[key][0]
        elif(decoded_values[key] != None and (key != 'old_search_id' )):
            column = column + key + ','
            values = values + "'" + str(decoded_values[key]) + "'" + ','
        elif(decoded_values[key] != None and key == 'old_search_id'):
            s ='select aql,mql from search_history where old_search_id = '
            s = s + decoded_values[key]
            queries_mql['old query'] = s 
        if(key == 'mql' and decoded_values[key] != None):
            queries_mql['new query'] = decoded_values[key]
    column = column.strip(',')
    values = values.strip(',')
    column = '(' + column + ')'
    values = '(' + values + ')'
    query = 'insert into search_history ' + column + ' ' +  'values ' + values
    queries_mql['insert query'] = query
    for k in queries_mql.keys():
        if(k == 'insert query'):
            engine = database_connector()
            with engine.connect() as con:
                con.execute(queries_mql[k])
        elif(k == 'old query'):
            engine = database_connector()
            with engine.connect() as con:
                result = con.execute(queries_mql[k])
                for row in result:
                    if(row[0] != None):
                        queries_aql[k] = row[0]
                    if(row[1] != None):
                        queries_mql[k] = row[1]
    if('insert query' in queries_mql.keys()):
        del queries_mql['insert query']
    return queries_mql,queries_aql

def response_mql(queries_mql):
    global result
    engine = database_connector()
    for k in queries_mql.keys():
        with engine.connect() as con:
            temp_result = con.execute(queries_mql[k])
            column = temp_result.keys()
            column = list(column)
            for row in temp_result:
                row = list(row)
                dict1 =dict()
                for i in range(len(column)):
                    dict1[column[i]] = row[i]
                result.append(dict1)
    return None
def response_aql(queries_aql):
    global result
    sizes = []
    url = 'http://100.26.220.250:8080/api/search?query='
    for k in queries_aql.keys():
        query = queries_aql[k]
        print(query)
        if(len(query) == 1):
            q = query[0]
            temp = url
            temp = temp + urllib.parse.quote(q)
            print(temp)
            temp_result = requests.get(temp)
            result.append(temp_result)
            return None
        else:
            if(('size' not in query[0]) or ('size' not in query[1])):
                for q in query:
                    temp = url
                    temp = temp + urllib.parse.quote(q)
                    temp_result = requests.get(temp)
                    temp_result = temp_result.json()
                    result.append(temp_result)
                return None
            else:
                temp0 = url + urllib.parse.quote(query[0])
                temp1 = url + urllib.parse.quote(query[1])
                temp_result0 = requests.get(temp0)
                temp_result0 = temp_result0.json()
                temp_result1 = requests.get(temp1)
                temp_result1 = temp_result1.json()
                temp_result = dict()
                temp_result['hits'] = []
                for hit in temp_result0['hits']:
                    sizes.append(hit['content']['size'])
                total = 0
                for hit in temp_result1['hits']:
                    if(hit['content']['size'] in sizes):
                        total = total + 1 
                        temp_result['hits'].append(hit)
                temp_result['total'] = total
                result.append(temp_result)
                return None


def response(queries_mql,queries_aql):
    global result
    result = []
    t1 = Thread(target = response_mql,args = (queries_mql,))
    t2 = Thread(target = response_aql,args = (queries_aql,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    return result


app = flask.Flask(__name__)
@app.route("/rest/search",methods=['POST'])
def hello():
    request = flask.request
    decoded_values = DataPreprocess(request)
    if(decoded_values == 'Invalid Method' ):
        return decoded_values,400
    elif(decoded_values == 'bad_aql_query'):
        return decoded_values,400
    elif(decoded_values == 'bad_sql_query'):
        return decoded_values,400
    table_creator()
    queries_mql,queries_aql = fetcher(decoded_values)
    result = response(queries_mql,queries_aql)
    return str(result)
    return flask.jsonify({"results":result})
    
if __name__ == "__main__": 
    app.run(host='0.0.0.0',debug = True)

