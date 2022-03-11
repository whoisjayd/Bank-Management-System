import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydb_test"
)
mycursor = mydb.cursor()
q = "DELETE FROM test_tt WHERE address = 'New Road City'"
mycursor.execute(q)
mydb.commit()
print(mycursor.rowcount, "record(s) deleted")
