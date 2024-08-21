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
        collection = db['suppliers']

        product_id = event.get('pathParameters', {}).get('id')
        if not product_id:
            return {
                "statusCode": 400,
                "headers": headers_open,
                "body": json.dumps({
                    "message": "El ID del proveedor es requerido en la URL"
                })
            }

        if not ObjectId.is_valid(product_id):
            return {
                "statusCode": 400,
                "headers": headers_open,
                "body": json.dumps({
                    "message": f"El ID del proveedor '{product_id}' no es válido."
                })
            }

        result = collection.delete_one({"_id": ObjectId(product_id)})

        if result.deleted_count > 0:
            return {
                "statusCode": 200,
                "headers": headers_open,
                "body": json.dumps({
                    "message": "Provedor eliminado correctamente"
                }, indent=2)
            }
        else:
            return {
                "statusCode": 404,
                "headers": headers_open,
                "body": json.dumps({
                    "message": "No se encontró el provedor con el ID proporcionado"
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
