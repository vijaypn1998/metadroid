from flask import Flask,request,jsonify
import urllib.parse
import query
import mysql.connector
import json

with open("config.json") as f:
    conf=json.load(f)

app = Flask(__name__)
@app.route("/rest/search",methods=['POST'])
def hello():
    if request.method == 'POST':
        mql=request.form['mql']
        decoded_mql=urllib.parse.unquote_plus(mql)
        decoded_mql=decoded_mql.strip('\n') 
        mysql_query=query.generate_query(decoded_mql)
        
        mydb = mysql.connector.connect(
         host=conf["host"],#"18.219.186.156",
         user=conf["user"],#"metadroid",
         password=conf["password"],#"Hashcrack#1",
         database=conf["database"]#"database_1"
        )

        mycursor = mydb.cursor(dictionary=True)
        try:
            mycursor.execute(mysql_query)
            myresult = mycursor.fetchall()
       
        except:
            return "Invalid MQL", 400
    
        return jsonify({"apps":myresult})
     
    
        
if __name__ == "__main__":
    app.run(host='0.0.0.0')
