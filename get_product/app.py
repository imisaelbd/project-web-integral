import json
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb+srv://misaelbd:Kk6n.c27JN.RSLK@mongodb-mbd.fqz75ib.mongodb.net/?retryWrites=true&w=majority&appName=MongoDB-MBD')


def lambda_handler(event, __):
    try:
        db = client['project-web-integral']
        collection = db['products']

        product_id = event.get('pathParameters', {}).get('id')
        if not product_id:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "El ID del producto es requerido en la ruta de la URL"
                })
            }

        if not ObjectId.is_valid(product_id):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": f"'{product_id}' no es un ObjectId válido. Debe ser una cadena hexadecimal de 24 caracteres."
                })
            }

        product = collection.find_one({"_id": ObjectId(product_id)})

        if product:
            product['_id'] = str(product['_id'])
            product['supplier'] = str(product['supplier'])
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Producto encontrado",
                    "product": product
                }, indent=2)
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "message": "No se encontró el producto con el ID proporcionado"
                })
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": str(e)
            })
        }