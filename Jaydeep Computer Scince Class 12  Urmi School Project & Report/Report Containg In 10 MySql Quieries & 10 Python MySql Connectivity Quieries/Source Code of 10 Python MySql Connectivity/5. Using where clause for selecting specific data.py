import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydb_test"
)
mycursor = mydb.cursor()
q = "SELECT * FROM test_tt WHERE address ='New City'"
mycursor.execute(q)
myresult = mycursor.fetchall()
if len(myresult) == 0:
    print("There is no such value !")
else:
    for x in myresult:
        print(x)
