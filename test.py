import pandas as pd
import sqlite3
import time
import subprocess

def filtrar_datos_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    filtered_data = []

    for line in lines:
        line = line.strip()
        items = line.split(',')

        data = {}
        for item in items:
            key, value = item.split('=')
            data[key.strip()] = value.strip().strip("'")

        filtered_data.append({
            'InvoiceId': int(data['Id']),
            'CustomerId': int(data['CustomerId']),
            'InvoiceDate': data['InvoiceDate'],
            'BillingAddress': data['BillingAddress'],
            'BillingCity': data['City'],
            'BillingState': data['BillingState'],
            'BillingCountry': data['BillingCountry'],
            'BillingPostalCode': data['BillingPostalCode'],
            'Total': float(data['Total']),
        })

    df_filtrado = pd.DataFrame(filtered_data)
    return df_filtrado

def procesar_csv_y_subir(file_path, db_path):
    df_filtrado = filtrar_datos_csv(file_path)

    # Detener Grafana
    subprocess.call(['net', 'stop', 'grafana'])  # Cambiar el nombre del servicio si es necesario

    # Conectar a la base de datos SQLite
    conn = sqlite3.connect(db_path, timeout=10)  # Aumenta el tiempo de espera
    cursor = conn.cursor()

    try:
        # Habilitar el modo WAL
        cursor.execute("PRAGMA journal_mode=WAL;")
        # Preparar la consulta de inserción
        insert_query = """
        INSERT INTO invoices (InvoiceId, CustomerId, InvoiceDate, BillingAddress, BillingCity, BillingState, BillingCountry, BillingPostalCode, Total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Insertar cada registro en la base de datos
        for index, row in df_filtrado.iterrows():
            while True:
                try:
                    cursor.execute(insert_query, (row['InvoiceId'], row['CustomerId'], row['InvoiceDate'], row['BillingAddress'], row['BillingCity'], row['BillingState'], row['BillingCountry'], row['BillingPostalCode'], row['Total']))
                    break  # Salir del bucle si se ejecutó correctamente
                except sqlite3.OperationalError as e:
                    if "database is locked" in str(e):
                        print("Base de datos bloqueada. Reintentando...")
                        time.sleep(1)  # Esperar un segundo antes de reintentar
                    else:
                        raise  # Lanzar otro tipo de error

        # Guardar los cambios
        conn.commit()
        print("Registros insertados exitosamente.")

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        # Cerrar la conexión
        conn.close()
    
    # Reiniciar Grafana
    subprocess.call(['net', 'start', 'grafana'])  # Cambiar el nombre del servicio si es necesario

# Rutas de los archivos
file_path = 'C:\\Users\\INSPIRON 15\\Desktop\\sourceXD.csv'  # Cambia esto a la ruta correcta de tu archivo CSV
db_path = 'C:\\Users\\INSPIRON 15\\Desktop\\chinook.db'  # Cambia esto a la ruta correcta de tu base de datos

# Procesar el CSV y subir los datos a la base de datos
procesar_csv_y_subir(file_path, db_path)
