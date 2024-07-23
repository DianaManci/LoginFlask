import MySQLdb

try:
    connection =MySQLdb.connect(
        host="localhost",
        user="root",
        password="",
        db="login"
    )

    print("conexion exitosa")
    connection.close()
except MySQLdb.Error as e:
    print(f"error:{e}")    