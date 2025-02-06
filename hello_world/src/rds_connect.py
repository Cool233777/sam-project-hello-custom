import pymysql
import os
from kms_helper import decrypt_rds_credentials

# Credenciales cifradas (las pegamos aquí o las tomamos de una variable de entorno)
ENCRYPTED_CREDENTIALS = os.getenv("ENCRYPTED_RDS_CREDENTIALS")

def lambda_handler(event, context):
    # Desencriptar credenciales
    rds_credentials = decrypt_rds_credentials(ENCRYPTED_CREDENTIALS)

    # Conectarse a RDS
    connection = pymysql.connect(
        host=rds_credentials["host"],
        user=rds_credentials["username"],
        password=rds_credentials["password"],
        database=rds_credentials["database"]
    )

    with connection.cursor() as cursor:
        cursor.execute("SELECT 'Conexion exitosa' AS message;")
        result = cursor.fetchone()

    return {
        "statusCode": 200,
        "body": result[0]
    }
