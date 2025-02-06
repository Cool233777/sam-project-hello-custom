import boto3
import base64
import json
import os

KMS_KEY_ID = os.getenv("KMS_KEY_ARN")

kms_client = boto3.client("kms")

def decrypt_rds_credentials(encrypted_credentials):
    try:
        # print(f"Encrypted Credentials: {encrypted_credentials[:50]}...")  # Solo imprime los primeros 50 caracteres
        # # 🚀 INTENTA PRIMERO SIN Base64 Decode
        # decrypted = kms_client.decrypt(
        #     CiphertextBlob=encrypted_credentials  # Directamente sin decodificar
        # )

        # # Decodificar los datos desencriptados
        # plaintext = decrypted['Plaintext'].decode('utf-8')
        # print(f"Decrypted JSON: {plaintext}")

        # # decrypted = kms_client.decrypt(
        # #     CiphertextBlob=base64.b64decode(encrypted_credentials)
        # # )
        # # return json.loads(decrypted['Plaintext'].decode('utf-8'))
        # return json.loads(plaintext)
        # Detectar si es Base64
        try:
            decoded_blob = base64.b64decode(encrypted_credentials)
        except Exception:
            decoded_blob = encrypted_credentials  # Si falla, es que ya está en binario
        
        decrypted = kms_client.decrypt(
            CiphertextBlob=decoded_blob
        )

        return json.loads(decrypted['Plaintext'].decode('utf-8'))
    except Exception as e:
        print(f"Error al desencriptar: {str(e)}")
        return None
