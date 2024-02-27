import mysql.connector 

dataBase = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "hiFri3nd!",
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE mariaDB")

print("all good")