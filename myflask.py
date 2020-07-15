from flask import Flask
import urllib.parse
import query
import mysql.connector
app = Flask(__name__)
@app.route("/rest/search",methods=['POST'])
def hello():
    if request.method == 'POST':
        mql=request.get_data()
        decoded_mql=urllib.parse.unqoute_plus(mql)
        mysql_query=query.generate_query(decoded_mql)

        mydb = mysql.connector.connect(
         host="18.219.186.156",
         user="metadroid",
         password="Hashcrack#1",
         database="database_1"
        )

        mycursor = mydb.cursor()

        mycursor.execute(mysql_query)

        myresult = mycursor.fetchall()
if __name__ == "__main__":
    app.run()
