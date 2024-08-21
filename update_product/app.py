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
        collection = db['products']

        product_id = event.get('pathParameters', {}).get('id')
        if not product_id:
            return {
                "statusCode": 400,
                "headers": headers_open,
                "body": json.dumps({
                    "message": "El ID del producto es requerido en la ruta de la URL"
                })
            }

        if not ObjectId.is_valid(product_id):
            return {
                "statusCode": 400,
                "headers": headers_open,
                "body": json.dumps({
                    "message": f"'{product_id}' no es un ObjectId válido. Debe ser una cadena hexadecimal de 24 caracteres."
                })
            }

        body = event.get('body')
        if not body:
            return {
                "statusCode": 400,
                "headers": headers_open,
                "body": json.dumps({
                    "message": "El cuerpo de la petición es requerido"
                })
            }

        data = json.loads(body)
        name = data.get('name')
        price = data.get('price')
        stock = data.get('stock')
        description = data.get('description')

        if not any([name, price, stock, description]):
            return {
                "statusCode": 400,
                "headers": headers_open,
                "body": json.dumps({
                    "message": "Al menos un campo (name, price, stock, description) es requerido para la actualización"
                })
            }

        update_fields = {}
        if name:
            update_fields['name'] = name
        if price:
            update_fields['price'] = price
        if stock:
            update_fields['stock'] = stock
        if description:
            update_fields['description'] = description

        result = collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_fields}
        )

        if result.modified_count > 0:
            return {
                "statusCode": 200,
                "headers": headers_open,
                "body": json.dumps({
                    "message": "Producto actualizado correctamente",
                    "updated_fields": update_fields
                }, indent=2)
            }
        else:
            return {
                "statusCode": 404,
                "headers": headers_open,
                "body": json.dumps({
                    "message": "No se encontró el producto con el ID proporcionado o no hubo cambios en la actualización"
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
