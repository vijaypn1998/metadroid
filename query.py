from rules import parser
import parsley
decoded_mql='publisher in ("Google", "VMware") AND "Creation Date" < -10m AND downloads > 1000 order by "Creation Date" DESC'
a,b=parser(decoded_mql)

query='''SELECT apk_id,title,creator,size
FROM Apk
WHERE '''
for i in range(len(a)-1):
    query = query + b[i]['column'] + b[i]['operator'] + b[i]['value'] + a[i]a[1]
i=len(a)-2
if(a[i][1] == 'order by'):
    query = query + '\n' + a[i][1] + b[i+1]['column'] + b[i+1]'[value'] 
else:
    query = query + b[i+1]['column'] +b[i+1]['operator'] + b[i+1]['value']