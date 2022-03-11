import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydb_test")
mycursor = mydb.cursor()
q = "ALTER TABLE test_tt DROP COLUMN Phone;"
mycursor.execute(q)
mydb.commit()
