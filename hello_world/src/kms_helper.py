import boto3
import base64
import json

KMS_KEY_ID = "arn:aws:kms:us-east-1:038462753284:key/e7f712a6-2273-4cfb-a97b-e5eac6d64c68"

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
