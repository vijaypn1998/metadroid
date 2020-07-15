import rules
def generate_query(decoded_mql):
    followed_by, req_dict = rules.parser(decoded_mql)
    mysql_query = 'SELECT apk_id,title,creator,installation_size FROM apk WHERE'
    i = 0
    if(len(followed_by)== 1):
        if (req_dict[i]['operator'] == 'in'):
                mysql_query = mysql_query + ' ' + req_dict[i]['column'] + ' ' + req_dict[i]['operator'] + ' (' + req_dict[i]['value'] + ') '
        else:
                mysql_query = mysql_query + ' ' + req_dict[i]['column'] + ' ' + req_dict[i]['operator'] + ' ' + req_dict[i]['value'] + ' ' 

        return mysql_query

    for i in range(len(followed_by) ):  
        if (followed_by[i] != None):
            if (req_dict[i]['operator'] == 'in'):
                mysql_query = mysql_query + ' ' + req_dict[i]['column'] + ' ' + req_dict[i]['operator'] + ' (' + req_dict[i]['value'] + ') ' + followed_by[i]
            else:
                mysql_query = mysql_query + ' ' + req_dict[i]['column'] + ' ' + req_dict[i]['operator'] + ' ' + req_dict[i]['value'] + ' ' + followed_by[i]
        else:
            if (req_dict[i]['operator'] == 'in'):
                mysql_query = mysql_query + ' ' + req_dict[i]['column'] + ' ' + req_dict[i]['operator'] + ' (' + req_dict[i]['value'] + ') '
            elif (req_dict[i]['value'] !=  None):
                mysql_query = mysql_query + ' ' + req_dict[i]['column'] + ' ' + req_dict[i]['operator'] + ' ' + req_dict[i]['value'] + ' '
            else:
                mysql_query = mysql_query + ' ' + req_dict[i]['column'] + ' ' + req_dict[i]['operator'] 

    return mysql_query


