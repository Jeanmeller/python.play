import cv2                          # acceso a camara
from pyzbar.pyzbar import decode    # decodifica el codigo de barras
import psycopg2                     # conexion a SQL

#  CONEXIÓN A LA BASE DE DATOS
conn = psycopg2.connect(
    dbname="DB_prueba",      
    user="soporte",     
    password="soporte", 
    host="localhost",     
    port="5432"
)
cur = conn.cursor()                 # cursor que permite comandos sql()

#  ESCÁNER DE CÓDIGO DE BARRAS CON CÁMARA
cap = cv2.VideoCapture(0)
print("📷 Cámara activada. Escanea un código de barras...")

codigo_leido = None                 # variable almacena codigo scaneado

while True:                         # bucle hasta que se scanee o press esc
    ret, frame = cap.read()         # captura el frame(img)
    if not ret:                     # ret es falso si la camara falla
        break

    # Escanea el código
    for barcode in decode(frame):                       # img capturada en barcode y sus atrib(data, type, rect)
        codigo_leido = barcode.data.decode('utf-8')        # decodifica el codigo
        print(f"✅ Código escaneado: {codigo_leido}")
        cap.release()                                   # libera la cámara
        cv2.destroyAllWindows()                         # cierra ventana de la cámara   
        break

    cv2.imshow("Escáner de código de barras", frame)    # muestra la imagen en una ventana

    if cv2.waitKey(1) == 27 or codigo_leido:             # ESC o escaneado
        break

#  BÚSQUEDA EN LA BASE DE DATOS 
if codigo_leido:                            # consulta sql y join 
    cur.execute("""         
        SELECT p."Nombre", p."Precio", p."Stock", p."categoria", p."estado_stock" 
        FROM productos p
        JOIN codigos_barras c ON p."ID" = c.producto_id
        WHERE c.codigo = %s    
    """, (codigo_leido,))                   # %s viene a ser el codigo_leido

    resultado = cur.fetchone()              # trae los datos

if resultado:                               
    nombre = resultado[0]
    precio = resultado[1]
    stock = resultado[2]
    categoria = resultado[3]
    estado = resultado[4] 

    icono_estado = {
        'rojo': '🔴',
        'naranja': '🟠',
        'verde': '🟢'
    }.get(estado.lower(), '⚪')             # por si hay valores no esperados

    print("\n📦 Producto encontrado:")
    print(f"🔹 Nombre: {nombre}")
    print(f"💰 Precio: {precio} soles")
    print(f"📦 Stock: {stock}")
    print(f"🏷️ Categoría: {categoria}")
    print(f"📊 Estado de stock: {icono_estado} {estado.capitalize()}")      #c capitalize trae la primera letra en mayus
else:
    print("❌ Producto no encontrado.")
