import mysql.connector 

dataBase = mysql.connector.connect(
    host = "django-crm-zvly.onrender.com",
    user = "root",
    passwd = "hiFri3nd!",
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE mariaDB")

print("all good")