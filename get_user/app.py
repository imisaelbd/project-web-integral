import json
from pymongo import MongoClient
from bson import ObjectId

headers_open = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Methods': 'GET,PUT, PATCH, POST,DELETE,OPTIONS',
    }

client = MongoClient('mongodb+srv://misaelbd:Kk6n.c27JN.RSLK@mongodb-mbd.fqz75ib.mongodb.net/?retryWrites=true&w=majority&appName=MongoDB-MBD')


def lambda_handler(event, __):
    try:
        db = client['project-web-integral']
        collection = db['users']

        user_id = event.get('pathParameters', {}).get('id')
        if not user_id:
            return {
                "statusCode": 400,
                "headers": headers_open,
                "body": json.dumps({
                    "message": "El ID del usuario es requerido en la ruta de la URL"
                })
            }

        if not ObjectId.is_valid(user_id):
            return {
                "statusCode": 400,
                "headers": headers_open,
                "body": json.dumps({
                    "message": f"'{user_id}' no es un ObjectId válido. Debe ser una cadena hexadecimal de 24 caracteres."
                })
            }

        user = collection.find_one({"_id": ObjectId(user_id)})

        if user:
            user['_id'] = str(user['_id'])
            return {
                "statusCode": 200,
                "headers": headers_open,
                "body": json.dumps({
                    "message": "Usuario encontrado",
                    "user": user
                }, indent=2)
            }
        else:
            return {
                "statusCode": 404,
                "headers": headers_open,
                "body": json.dumps({
                    "message": "No se encontró el usuario con el ID proporcionado"
                })
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers_open,
            "body": json.dumps({
                "message": str(e)
            })
        }
