import boto3
import json
from kms_helper import decrypt_password

secrets_client = boto3.client("secretsmanager")

SECRET_NAME = "rds-user-credentials"

def lambda_handler(event, context):
    body = json.loads(event["body"])
    username = body["username"]
    password = body["password"]

    # Obtener usuario guardado
    response = secrets_client.get_secret_value(SecretId=SECRET_NAME)
    stored_user = json.loads(response["SecretString"])

    if stored_user["username"] == username:
        decrypted_password = decrypt_password(stored_user["password"])
        
        if decrypted_password == password:
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Login successful"})
            }
    
    return {
        "statusCode": 401,
        "body": json.dumps({"message": "Invalid credentials"})
    }
