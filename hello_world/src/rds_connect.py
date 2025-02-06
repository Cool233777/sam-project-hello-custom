import pymysql
import os
import json
from kms_helper import decrypt_rds_credentials
import logging

# Credenciales cifradas (las pegamos aquí o las tomamos de una variable de entorno)
ENCRYPTED_CREDENTIALS = os.getenv("ENCRYPTED_RDS_CREDENTIALS")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        connection = pymysql.connect(
            host="rds-test-identifier.cp0mi64yu2ef.us-east-1.rds.amazonaws.com",
            user="admin",
            password="Overwatch1081718(",
            database="usuarios",
            port=3306,
            connect_timeout=5
        )
        logger.info("Conexión a RDS exitosa")
        connection.close()
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Conexión exitosa a RDS"})
        }
    except Exception as e:
        logger.error(f"Error en la conexión a RDS: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Error en la conexión a RDS: {str(e)}"})
        }
    # if not ENCRYPTED_CREDENTIALS:
    #     return {
    #         "statusCode": 500,
    #         "body": json.dumps({"error": "No hay credenciales encriptadas en la variable de entorno"})
    #     }

    # # Desencriptar credenciales
    # rds_credentials = decrypt_rds_credentials(ENCRYPTED_CREDENTIALS)
    
    # if not rds_credentials:
    #     return {
    #         "statusCode": 500,
    #         "body": json.dumps({"error": "No se pudieron desencriptar las credenciales"})
    #     }
    # # Loguear las credenciales (Asegúrate de no loguear las contraseñas en entornos de producción)
    # logger.info(f"Conectando a RDS con host: {rds_credentials["host"]}, usuario: {rds_credentials["username"]}, base de datos: {rds_credentials["database"]}")

    # try:
    #     # Conectarse a RDS
    #     connection = pymysql.connect(
    #         host=rds_credentials["host"],
    #         user=rds_credentials["username"],
    #         password=rds_credentials["password"],
    #         database=rds_credentials["database"],
    #         port=3306,
    #         connect_timeout=5,  # Evita que se quede esperando
    #     )

    #     with connection.cursor() as cursor:
    #         cursor.execute("SELECT 'Conexion exitosa' AS message;")
    #         result = cursor.fetchone()

    #     # Cerrar la conexión
    #     connection.close()

    #     return {
    #         "statusCode": 200,
    #         "body": json.dumps({"message": result[0]})
    #     }

    # except Exception as e:
    #     logger.error(f"Error al conectarse a la base de datos: {str(e)}")
    #     return {
    #         "statusCode": 500,
    #         "body": json.dumps({"error": f"Error en la conexión a RDS: {str(e)}"})
    #     }

    # finally:
    #     if 'connection' in locals():
    #         connection.close()  # Cierra la conexión si se creó
