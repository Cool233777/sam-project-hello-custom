import boto3
import base64
import json
import os

KMS_KEY_ID = os.getenv("KMS_KEY_ARN")

kms_client = boto3.client("kms")

def decrypt_rds_credentials(encrypted_credentials):
    try:
        # Detectar si ya está en Base64
        if isinstance(encrypted_credentials, str):
            print(f"🔍 Input antes de decodificar: {encrypted_credentials[:50]}...")  # Solo muestra los primeros 50 caracteres
            encrypted_credentials = base64.b64decode(encrypted_credentials)

        # Desencriptar con KMS
        decrypted = kms_client.decrypt(
            CiphertextBlob=encrypted_credentials
        )

        plaintext = decrypted['Plaintext'].decode('utf-8')
        print(f"🔓 Datos desencriptados: {plaintext}")  # 🚀 Esto debería ser JSON con credenciales

        return json.loads(plaintext)
    except Exception as e:
        print(f"Error al desencriptar: {str(e)}")
        return None
