import {
    SecretsManagerClient,
    GetSecretValueCommand,
  } from "@aws-sdk/client-secrets-manager";

 

export const secretManager = async () => {
    const secret_name = "conexion/rds/a/chejo";

    const client = new SecretsManagerClient({
    region: "us-east-1",
    });
  
    let response;
  
    try {
            console.log("Obteniendo secret manager");
            response = await client.send(
                new GetSecretValueCommand({
                SecretId: secret_name
                //VersionStage: "AWSCURRENT", // VersionStage defaults to AWSCURRENT if unspecified
            }));
            console.log("Secret manager obtenido?");
            console.log(response);
    } catch (error) {
        console.log('entro aca')
        console.log(error)
        throw error;
    }
    console.log("Secret manager obtenido?v2");
    const secret = response.SecretString;
    return secret;
}