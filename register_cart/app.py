import json
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb+srv://misaelbd:Kk6n.c27JN.RSLK@mongodb-mbd.fqz75ib.mongodb.net/?retryWrites=true&w=majority&appName=MongoDB-MBD')


def lambda_handler(event, __):
    try:
        db = client['project-web-integral']
        carts_collection = db['carts']
        users_collection = db['users']

        id_user = event.get('pathParameters', {}).get('id')
        if not id_user:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "El campo 'id' es requerido en la URL"
                })
            }

        if not ObjectId.is_valid(id_user):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": f"El ID del usuario '{id_user}' no es válido."
                })
            }

        user = users_collection.find_one({"_id": ObjectId(id_user)})
        if not user:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "message": f"El usuario con el ID '{id_user}' no existe."
                })
            }

        existing_cart = carts_collection.find_one({"user.$id": ObjectId(id_user)})
        if existing_cart:
            existing_cart['_id'] = str(existing_cart['_id'])
            existing_cart['user'] = id_user
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Ya existe un carrito para este usuario",
                    "cart": existing_cart
                }, indent=2)
            }

        cart = {
            'user': {
                '$ref': 'users',
                '$id': ObjectId(id_user)
            },
            'total': 0,
            'products': []
        }

        result = carts_collection.insert_one(cart)

        if result.inserted_id:
            cart['_id'] = str(result.inserted_id)
            cart['user'] = id_user
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Carrito creado correctamente",
                    "cart": cart
                }, indent=2)
            }
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "message": "Error al crear el carrito"
                })
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": str(e)
            })
        }
