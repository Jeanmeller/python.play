import psycopg2     #conexion a SQL
import barcode      # genera codigos de barras
from barcode.writer import ImageWriter  #gerana img.

# Conexión a la base de datos
conn = psycopg2.connect(
    dbname="DB_prueba",
    user="soporte",
    password="soporte",
    host="localhost",
    port="5432"
)
cur = conn.cursor() #cursor permite comandos sql()

# Traer códigos EAN desde la tabla
cur.execute("SELECT producto_id, codigo FROM codigos_barras")
registros = cur.fetchall()      #guarda todo info en tabla y tupla(2)

# Crear los códigos de barras
for producto_id, codigo in registros:
    ean = barcode.get('ean13', codigo, writer=ImageWriter())
    nombre_archivo = f"codigo_producto_{producto_id}"
    ean.save(nombre_archivo)  # Guarda como PNG

print("¡Códigos de barras generados con éxito!")

# Cierre de conexión
cur.close()
conn.close()
