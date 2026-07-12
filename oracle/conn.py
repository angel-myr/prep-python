import oracledb

connection = oracledb.connect(
    user="magno",
    password="ree",
    host="localhost",
    port=1521,
    service_name="DAA2002"
)

print("Conectado correctamente")