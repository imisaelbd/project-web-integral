import json
import boto3
from botocore.exceptions import ClientError

# Configura los valores según tu configuración
client_id = "iocn20os51ea9of20bu4jg362"
user_pool_id = 'us-east-1_0CdCxDU3u'

headers_open = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,OPTIONS',
}

def lambda_handler(event, context):
    client = boto3.client('cognito-idp', region_name='us-east-1')
    try:
        body_parameters = json.loads(event["body"]) if isinstance(event["body"], str) else event["body"]
        username = body_parameters.get('username')
        password = body_parameters.get('password')

        # Realiza la autenticación del usuario sin SECRET_HASH
        response = client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )

        # Verifica si la respuesta contiene el campo 'AuthenticationResult'
        if 'AuthenticationResult' in response:
            id_token = response['AuthenticationResult']['IdToken']
            access_token = response['AuthenticationResult']['AccessToken']
            refresh_token = response['AuthenticationResult']['RefreshToken']

            # Obtén los grupos del usuario
            user_groups = client.admin_list_groups_for_user(
                Username=username,
                UserPoolId=user_pool_id
            )

            # Determina el rol basado en el grupo
            role = None
            if user_groups['Groups']:
                role = user_groups['Groups'][0]['GroupName']  # Asumiendo un usuario pertenece a un solo grupo

            return {
                'statusCode': 200,
                'headers': headers_open,
                'body': json.dumps({
                    'id_token': id_token,
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'role': role
                })
            }
        else:
            raise Exception("Missing 'AuthenticationResult' in response")
    except ClientError as e:
        print(f"ClientError: {e.response['Error']['Message']}")
        return {
            'statusCode': 400,
            'headers': headers_open,
            'body': json.dumps({"error_message": e.response['Error']['Message']})
        }
    except Exception as e:
        print(f"Exception: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers_open,
            'body': json.dumps({"error_message": str(e)})
        }
