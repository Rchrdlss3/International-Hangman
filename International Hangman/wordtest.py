import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="ZTIwpEp646939",
    database="UserInfos"
    )
cursor = db.cursor()
username= "Rchrdlss3"
password = "ZTIwpEp646939"
sql = "SELECT * FROM userinfo WHERE BINARY username = '%s' AND BINARY userpassw = '%s'" %(username,password)
cursor.execute(sql)
x = cursor.fetchone()
print(x)
print(type(x[1]))
print(x[3])
print(type(int(x[3])))