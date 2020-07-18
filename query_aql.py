import rules_aql
decoded_aql =''''text'='"cake recipe"~81' AND 'size'='>100K AND <10G' AND 'when'='yesterday' AND  'filename'='*.jpg' OR 'size'='<1000G' AND 'filename'='goobe.text' '''
def normal_query(dict1):
    query = ''
    query = query + dict1['column'] + ':' + dict1['value'] + ' '
    return query
def text_query(dict1):
    query = ''
    query = query + dict1['value'] + ' '
    return query
def size_split(dict1):
    list1 = dict1['value'].split(' ')
    number_comparisions = list1.count('AND') + 1
    j = 1
    i = 0
    query = ''
    while( i < len(list1) and j <= number_comparisions):
        query = query + dict1['column'] + list1[i] + ' '
        i = i + 2
        j = j + 1
    return query

def aql_generate_query(decoded_aql):
    followed_by,req_dict= rules_aql.aql_parser(decoded_aql)
    num_queries = followed_by.count('OR') + 1
    queries = [''] * num_queries
    query = ''
    query_index = 0
    i = 0
    while( i < len(followed_by)):
        if(followed_by[i] == 'AND'):
            if(req_dict[i]['column'] == 'text'):
                query = query + text_query(req_dict[i])
            elif(req_dict[i]['column'] == 'size'):
                query = query + size_split(req_dict[i])
            else:
                query = query + normal_query(req_dict[i])
        elif(followed_by[i] == 'OR'):
            if(req_dict[i]['column'] == 'text'):
                query = query + text_query(req_dict[i])
                queries[query_index] = query
                query = ''
                query_index = query_index + 1
            elif(req_dict[i]['column'] == 'size'):
                query = query + size_split(req_dict[i])
                queries[query_index] = query
                query = ''
                query_index = query_index + 1
            else:
                query = query + normal_query(req_dict[i])
                queries[query_index] = query
                query = ''
                query_index = query_index + 1
        elif(followed_by[i] == None):
            if(req_dict[i]['column'] == 'text'):
                query = query + text_query(req_dict[i])
                queries[query_index] = query
            elif(req_dict[i]['column'] == 'size'):
                query = query + size_split(req_dict[i])
                queries[query_index] = query
            else:
                query = query + normal_query(req_dict[i])
                queries[query_index] = query
        i = i + 1
    return queries
decoded_aql=decoded_aql.strip(' ')
a = "'source'='dropbox' AND 'size'='>100K' OR 'size'='>10G'"
queries = aql_generate_query(decoded_aql)
for x in queries:
    print(x)
