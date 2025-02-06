import boto3
import base64
import json
import os

KMS_KEY_ID = os.getenv("KMS_KEY_ARN")

kms_client = boto3.client("kms")

def decrypt_rds_credentials(encrypted_credentials):
    try:
        decrypted = kms_client.decrypt(
            CiphertextBlob=base64.b64decode(encrypted_credentials)
        )
        return json.loads(decrypted['Plaintext'].decode('utf-8'))
    except Exception as e:
        print(f"Error al desencriptar: {str(e)}")
        return None
