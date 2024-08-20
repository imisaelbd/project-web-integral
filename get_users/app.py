import json
import jwt
from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://misaelbd:Kk6n.c27JN.RSLK@mongodb-mbd.fqz75ib.mongodb.net/?retryWrites=true&w=majority&appName=MongoDB-MBD')


def lambda_handler(event, __):
    try:
        token = event['headers']['Authorization'].split()[1]

        decoded_token = jwt.decode(
            token, options={"verify_signature": False}
        )

        role = decoded_token.get('cognito:groups', [''])[0]


        db = client['project-web-integral']
        collection = db['users']

        users = list(collection.find({}))

        for user in users:
            user['_id'] = str(user['_id'])

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Usuarios encontrados",
                "users": users,
                "role": role
            }, indent=2)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": str(e)
            })
        }
