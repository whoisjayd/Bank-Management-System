import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydb_test"
)
mycursor = mydb.cursor()
mycursor.execute(
    "CREATE TABLE test_tt (name VARCHAR(255) DEFAULT '-', address VARCHAR(255))")
