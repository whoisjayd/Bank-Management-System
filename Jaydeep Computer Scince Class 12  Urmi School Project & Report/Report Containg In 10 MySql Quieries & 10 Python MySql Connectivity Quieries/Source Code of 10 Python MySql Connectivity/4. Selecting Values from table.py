import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydb_test"
)
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM test_tt")
myresult = mycursor.fetchall()
for x in myresult:
    print(x)
