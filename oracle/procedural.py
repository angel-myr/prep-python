import oracledb
import datetime
import pandas as pd

dsn = oracledb.makedsn(
    "localhost",
    1521,
    service_name="DAA2002"
)

connection = oracledb.connect(
    user="magno",
    password="ree",
    dsn=dsn
)

# Ejecutar una consulta
cursor = connection.cursor()

cursor.execute("""
    SELECT *
    FROM EMPLEADOS
""")

for fila in cursor:
    print(fila)

filas = cursor.fetchall()
print(filas)

# Solo un registro
cursor.execute("""
    SELECT *
    FROM EMPLEADOS
    WHERE ID = :id
    AND SUELDO > :ran
""",
    id=3,
    ran=1000.00
)

empleado = cursor.fetchone()
print(empleado)

# Ejecutar INSERT
cursor.execute("""
    INSERT INTO empleados(
        nombre,
        sueldo
    )
    VALUES(
        :nombre,
        :sueldo
    )
""",
    nombre="Carlos",
    sueldo=5000
)

connection.commit()

# Ejecutar PROCEDURE
cursor.callproc(
    "ACTUALIZAR_SALDOS",
    [datetime.date.today()]
)

cursor.callproc(
    "CREAR_CLIENTE",
    [
        "Angel",
        22
    ]
)

connection.commit()

# Ejecutar FUNCIÓN
resultado = cursor.callfunc(
    "OBTENER_TOTAL",
    int,
    [6]
)

print(resultado)

# Para PANDAS
query = """
    SELECT *
    FROM EMPLEADOS
"""

df = pd.read_sql(query, connection)
print(df.head())

# Desconexión BD
cursor.close()
connection.close()