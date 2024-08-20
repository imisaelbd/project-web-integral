import json
import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, __):
    client = boto3.client('cognito-idp', region_name='us-east-1')
    client_id = "7spm11b94qt7oa3r25ol9j80st"

    try:
        body_parameters = json.loads(event["body"])
        username = body_parameters.get('username')
        password = body_parameters.get('password')

        response = client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )

        id_token = response['AuthenticationResult']['IdToken']
        access_token = response['AuthenticationResult']['AccessToken']
        refresh_token = response['AuthenticationResult']['RefreshToken']

        # Obtiene los grupos de usuarios
        user_groups = client.admin_list_groups_for_user(
            Username=username,
            UserPoolId='us-east-1_lGjX24BuI'  # Reemplaza con tu User Pool ID
        )

        # Determina el rol por el grupo al que pertenece el usuario
        role = None
        if user_groups['Groups']:
            role = user_groups['Groups'][0]['GroupName']  # Asumiendo un usuario pertenece a un solo grupo

        return {
            'statusCode': 200,
            'body': json.dumps({
                'id_token': id_token,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'role': role
            })
        }

    except ClientError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"error_message": e.response['Error']['Message']})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"error_message": str(e)})
        }