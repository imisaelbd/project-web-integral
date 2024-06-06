import json
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb+srv://misaelbd:Kk6n.c27JN.RSLK@mongodb-mbd.fqz75ib.mongodb.net/?retryWrites=true&w=majority&appName=MongoDB-MBD')


def lambda_handler(event, __):
    try:
        db = client['project-web-integral']
        collection = db['users']

        user_id = event.get('pathParameters', {}).get('id')
        if not user_id:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "El ID del usuario es requerido en la URL"
                })
            }

        if not ObjectId.is_valid(user_id):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": f"El ID del usuario '{user_id}' no es válido."
                })
            }

        result = collection.delete_one({"_id": ObjectId(user_id)})

        if result.deleted_count > 0:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Usuario eliminado correctamente"
                }, indent=2)
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "message": "No se encontró el usuario con el ID proporcionado"
                })
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": str(e)
            })
        }
