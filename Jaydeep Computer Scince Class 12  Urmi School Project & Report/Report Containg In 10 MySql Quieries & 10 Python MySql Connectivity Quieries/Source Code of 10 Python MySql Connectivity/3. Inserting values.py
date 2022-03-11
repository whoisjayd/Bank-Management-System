import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydb_test"
)
mycursor = mydb.cursor()
q = "INSERT INTO test_tt (name, address) VALUES (%s, %s)"
val = ("Jaydeep", "New Road City")
mycursor.execute(q, val)
mydb.commit()
print(mycursor.rowcount, "record inserted.")
