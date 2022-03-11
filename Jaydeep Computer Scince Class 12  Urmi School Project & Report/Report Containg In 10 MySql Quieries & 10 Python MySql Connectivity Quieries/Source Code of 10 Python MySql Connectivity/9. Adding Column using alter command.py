import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydb_test"
)
mycursor = mydb.cursor()
q = "ALTER TABLE test_tt ADD Phone VARCHAR(100) DEFAULT '-'"
mycursor.execute(q)
mydb.commit()
