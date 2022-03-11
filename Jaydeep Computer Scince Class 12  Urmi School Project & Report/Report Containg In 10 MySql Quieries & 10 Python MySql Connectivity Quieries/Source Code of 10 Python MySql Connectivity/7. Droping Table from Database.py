import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydb_test"
)
mycursor = mydb.cursor()
q = "DROP TABLE test_tt"
mycursor.execute(q)
