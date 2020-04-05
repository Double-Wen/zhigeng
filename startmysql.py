import pymysql
connection = pymysql.connect(
    host="mysql.liuwenwen.net",
    port=10136,
    user="root",
    database="zhigeng",
    password="Ali123456",
    charset="utf8"
)
cursor = connection.cursor()
sql = """select * from 版块名称代码表;"""
print(sql)
cursor.execute(sql)
result = cursor.fetchall()
print(type(result))
print(result)
cursor.close()
connection.close()
