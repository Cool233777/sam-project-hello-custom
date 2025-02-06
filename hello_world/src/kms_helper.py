import boto3
import base64
import json
import os

KMS_KEY_ID = os.getenv("KMS_KEY_ARN")

kms_client = boto3.client("kms")

def decrypt_rds_credentials(encrypted_credentials):
    try:
        #Detectar si ya está en Base64
        if isinstance(encrypted_credentials, str):
            print(f"🔍 Input antes de decodificar: {encrypted_credentials[:50]}...")  
            encrypted_credentials = base64.b64decode(encrypted_credentials)

        #Primera desencripción: AWS KMS
        decrypted = kms_client.decrypt(CiphertextBlob=encrypted_credentials)
        plaintext = decrypted['Plaintext'].decode('utf-8')

        print(f"Resultado KMS (aún Base64?): {plaintext[:50]}...")

        # Segunda desencripción: Base64 interna (si es necesario)
        try:
            decoded_json = base64.b64decode(plaintext).decode('utf-8')
            print(f"JSON final: {decoded_json}")
            return json.loads(decoded_json)
        except Exception as e:
            print(f"No estaba en Base64 interno, usando directamente")
            return json.loads(plaintext)
    except Exception as e:
        print(f"Error al desencriptar: {str(e)}")
        return None
