﻿from rules import parser
def query_generator(decoded_mql):
    a,b=parser(decoded_mql)
    query='''SELECT apk_id,title,creator,size
    FROM Apk
    WHERE'''
    space =" "
    for i in range(len(a)-1):
        if(i!=len(a)-2)):
            if(b[i][0]['operator']=='in'):
                query = query + space + b[i][0]['column'] + space + b[i][0]['operator'] + space + '(' + b[i][0]['value'] + ")" + space + a[i]a[1]
            else:
                query = query + space + b[i+1][0]['column'] + space +b[i+1][0]['operator'] + space + b[i+1][0]['value'] + space a[i]a[1]
        else:
            query = query + space + b[i+1][0]['column'] + space +b[i+1][0]['operator'] + space + b[i+1][0]['value']      
    i=len(a)-2
    if(a[i][1] == 'order by'):
        query = query + '\n' + a[i][1] + space + b[i+1][0]['column'] + space + b[i+1][0]'[value'] 
    else:
        query = query + space + b[i+1][0]['column'] + space +b[i+1][0]['operator'] + space + b[i+1][0]['value']
    return query
