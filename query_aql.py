import rules_aql
decoded_aql =''''size'='>10G AND <10K' AND  'text'='"cake recipe"~81' AND 'when'='yesterday' AND 'filename'='*.jpg' AND 'filename'='*/goobe/*.docs' '''
queries = []
def size_split(req_dict,followed_by,query,i):
    global queries
    list1 = req_dict[i]['value'].split(' ')
    j = 0
    while(j < len(list1)):
        temp_query = query
        temp = i
        temp_query = temp_query + req_dict[temp]['column'] + list1[j] + ' '
        temp = temp + 1
        while(temp < len(followed_by)):
            if(req_dict[temp]['column'] == 'text'):
                temp_query = temp_query + req_dict[temp]['value'] + ' '
            else:
                temp_query = temp_query + req_dict[temp]['column'] + ':' + req_dict[temp]['value'] + ' '
            temp = temp + 1
        queries.append(temp_query)
        j = j + 2
def aql_generate_query(decoded_aql):
    global queries
    count = 0 
    followed_by,req_dict = rules_aql.aql_parser(decoded_aql)
    queries = []
    query = ''
    i = 0
    while( i < len(followed_by)):
            if(req_dict[i]['column'] == 'text'):
                query = query + req_dict[i]['value'] + ' '
            elif(req_dict[i]['column'] == 'size'):
                size_split(req_dict,followed_by,query,i)
                count = 1
            else:
                query = query + req_dict[i]['column'] + ':' + req_dict[i]['value'] + ' ' 
            i = i + 1
    if(count != 1):
        queries.append(query)
    return queries
decoded_aql=decoded_aql.strip(' ')
queries = aql_generate_query(decoded_aql)
for x in queries:
    print(x)

