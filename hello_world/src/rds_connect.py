import pymysql
import os
import json
from kms_helper import decrypt_rds_credentials

# Credenciales cifradas (las pegamos aquí o las tomamos de una variable de entorno)
ENCRYPTED_CREDENTIALS = os.getenv("ENCRYPTED_RDS_CREDENTIALS")

def lambda_handler(event, context):
    if not ENCRYPTED_CREDENTIALS:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "No hay credenciales encriptadas en la variable de entorno"})
        }

    # Desencriptar credenciales
    rds_credentials = decrypt_rds_credentials(ENCRYPTED_CREDENTIALS)
    
    if not rds_credentials:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "No se pudieron desencriptar las credenciales"})
        }

    try:
        # Conectarse a RDS
        connection = pymysql.connect(
            host=rds_credentials["host"],
            user=rds_credentials["username"],
            password=rds_credentials["password"],
            database=rds_credentials["database"],
            connect_timeout=5  # Evita que se quede esperando
        )

        with connection.cursor() as cursor:
            cursor.execute("SELECT 'Conexion exitosa' AS message;")
            result = cursor.fetchone()

        return {
            "statusCode": 200,
            "body": json.dumps({"message": result[0]})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Error en la conexión a RDS: {str(e)}"})
        }

    finally:
        if 'connection' in locals():
            connection.close()  # Cierra la conexión si se creó
