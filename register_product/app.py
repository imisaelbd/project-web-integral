import json
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb+srv://misaelbd:Kk6n.c27JN.RSLK@mongodb-mbd.fqz75ib.mongodb.net/?retryWrites=true&w=majority&appName=MongoDB-MBD')


def lambda_handler(event, __):
    try:
        db = client['project-web-integral']
        products_collection = db['products']
        suppliers_collection = db['suppliers']

        body = event.get('body')
        if not body:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "El cuerpo en la petición es requerido"
                })
            }

        data = json.loads(body)
        name = data.get('name')
        price = data.get('price')
        stock = data.get('stock')
        description = data.get('description')
        id_supplier = data.get('id_supplier')

        if not name or not price or not stock or not description or not id_supplier:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Todos los campos son requeridos"
                })
            }

        if not ObjectId.is_valid(id_supplier):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": f"El ID del proveedor '{id_supplier}' no es válido."
                })
            }

        existing_product = products_collection.find_one({"name": name})
        if existing_product:
            existing_product['_id'] = str(existing_product['_id'])
            existing_product['supplier'] = str(existing_product['supplier'])
            return {
                "statusCode": 409,
                "body": json.dumps({
                    "message": f"El producto '{name}' ya existe en la base de datos",
                    "product": existing_product
                }, indent=2)
            }

        supplier = suppliers_collection.find_one({"_id": ObjectId(id_supplier)})
        if not supplier:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "message": f"El proveedor con el ID '{id_supplier}' no existe."
                })
            }

        product = {
            'name': name,
            'price': price,
            'stock': stock,
            'description': description,
            'supplier': {
                '$ref': 'suppliers',
                '$id': ObjectId(id_supplier)
            }
        }

        result = products_collection.insert_one(product)

        if result.inserted_id:
            product['_id'] = str(result.inserted_id)
            product['supplier'] = id_supplier
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Producto registrado correctamente",
                    "product": product
                }, indent=2)
            }
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "message": "Error al insertar el producto"
                })
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": str(e)
            })
        }