import mysql.connector as mysql

# connecting to the database using 'connect()' method
# it takes 3 required parameters 'host', 'user', 'passwd'
db = mysql.connect(
    host="192.168.0.101",
    user="usuario",
    passwd="jm",
    database = "umg_didactica"
)

cursor = db.cursor()

query = "INSERT INTO empleados (IdNumero, Nombre, Correo, Cumpleaños) VALUES (%s, %s, %s, %s)"
values = (989898989, 'Luis', 'luis@hola.com', '2021-05-19')
cursor.execute(query, values)

db.commit()

print(cursor.rowcount, "record inserted")