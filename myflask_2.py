from flask import Flask,request,jsonify
import mysql.connector
import json

with open("config.json") as f:
    conf=json.load(f)
def generator(apk_id):
    my_query = 'SELECT * FROM apk INNER JOIN screenshot ON apk.apk_id=screenshot.apk_id WHERE apk.apk_id = '
    my_query = my_query + apk_id
    return my_query

app = Flask(__name__)
@app.route("/rest/apk",methods=['GET'])
def hello():
    if request.method == 'GET':
        apk_id = request.args.get("apk_id")
        my_query = generator(apk_id)
        mydb = mysql.connector.connect(
         host=conf["host"],#"18.219.186.156",
         user=conf["user"],#"metadroid",
         password=conf["password"],#"Hashcrack#1",
         database=conf["database"]#"database_1"
        )

        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute(my_query)
        myresult = mycursor.fetchall()
        try:
            mycursor.execute(my_query)
            myresult = mycursor.fetchall()
       
        except:
            return "Invalid apk_id", 400
    
        return jsonify({"result":myresult})
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug = True)

