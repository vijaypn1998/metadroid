import rules_aql
decoded_aql ='text="code to search~81" AND filename="*/John-Recipe/goobe/*.jpg" AND dirname="directory name" OR age="date" AND source="google drive" OR author="Jason" AND size="<10M AND >10G"'
def aql_generate_query(decoded_aql):
    followed_by,req_dict= rules_aql.aql_parser(decoded_aql)
    num_queries = followed_by.count('OR') + 1
    queries = [''] * num_queries
    query = ''
    query_index = 0
    i = 0
    while( i < len(followed_by)):
        if(followed_by[i] == 'AND'):
            query = query + req_dict[i]['column'] + ':' + req_dict[i]['value'] + ' '
        elif(followed_by[i] == 'OR'):
            query = query +  req_dict[i]['column'] + ':' +  req_dict[i]['value']
            queries[query_index] = query
            query = ''
            query_index = query_index + 1
        elif(followed_by[i] == None):
            query = query +  req_dict[i]['column'] + ':' +  req_dict[i]['value']
            queries[query_index] = query
        i = i + 1
    return queries
