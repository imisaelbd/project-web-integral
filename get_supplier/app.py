import json
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb+srv://misaelbd:Kk6n.c27JN.RSLK@mongodb-mbd.fqz75ib.mongodb.net/?retryWrites=true&w=majority&appName=MongoDB-MBD')


def lambda_handler(event, __):
    try:
        db = client['project-web-integral']
        collection = db['suppliers']

        supplier_id = event.get('pathParameters', {}).get('id')
        if not supplier_id:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "El ID del proveedor es requerido en la ruta de la URL"
                })
            }

        if not ObjectId.is_valid(supplier_id):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": f"'{supplier_id}' no es un ObjectId válido. Debe ser una cadena hexadecimal de 24 caracteres."
                })
            }

        supplier = collection.find_one({"_id": ObjectId(supplier_id)})

        if supplier:
            supplier['_id'] = str(supplier['_id'])
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Proveedor encontrado",
                    "supplier": supplier
                }, indent=2)
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "message": "No se encontró el proveedor con el ID proporcionado"
                })
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": str(e)
            })
        }
