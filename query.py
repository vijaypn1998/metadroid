import rules
def generate_query(decoded_mql):
    a, b = rules_2.parser(decoded_mql)
    mysql_query = '''SELECT apk_id,title,creator,size
    FROM apk
    WHERE'''
    for i in range(len(a) - 1):
        if (i != len(a) - 2):
            if (b[i][0]['operator'] == 'in'):
                mysql_query = mysql_query + ' ' + b[i][0]['column'] + ' ' + b[i][0]['operator'] + ' (' + b[i][0][
                    'value'] + ') ' + a[i][1]
            else:
                mysql_query = mysql_query + ' ' + b[i][0]['column'] + ' ' + b[i][0]['operator'] + ' ' + b[i][0][
                    'value'] + ' ' + a[i][1]
        else:
            mysql_query = mysql_query + ' ' + b[i][0]['column'] + ' ' + b[i][0]['operator'] + ' ' + b[i][0]['value']

    i = len(a) - 2
    if (a[i][1] == 'ORDER BY'):
         mysql_query = mysql_query + '\n' + a[i][1] + ' ' + b[i + 1][0]['column'] + ' ' + b[i + 1][0]['operator']
    else:
        mysql_query = mysql_query + ' ' + b[i + 1][0]['column'] + ' ' + b[i + 1][0]['operator'] + ' ' + b[i + 1][0]['value']
    return mysql_query
