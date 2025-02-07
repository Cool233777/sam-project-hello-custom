import boto3
import json
from kms_helper import encrypt_password

secrets_client = boto3.client("secretsmanager")

SECRET_NAME = "rds-user-credentials"

def lambda_handler(event, context):
    body = json.loads(event["body"])
    username = body["username"]
    password = body["password"]

    encrypted_password = encrypt_password(password)

    new_user = {
        "username": username,
        "password": encrypted_password
    }

    secrets_client.put_secret_value(
        SecretId=SECRET_NAME,
        SecretString=json.dumps(new_user)
    )

    return {
        "statusCode": 201,
        "body": json.dumps({"message": "User registered successfully"})
    }
