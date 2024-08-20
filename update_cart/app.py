import json
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb+srv://misaelbd:Kk6n.c27JN.RSLK@mongodb-mbd.fqz75ib.mongodb.net/?retryWrites=true&w=majority&appName=MongoDB-MBD')


def lambda_handler(event, __):
    try:
        db = client['project-web-integral']
        carts_collection = db['carts']
        products_collection = db['products']

        cart_id = event.get('pathParameters', {}).get('id')
        if not cart_id:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "El campo ID del carrito es obligatorio en la URL"
                })
            }

        if not ObjectId.is_valid(cart_id):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": f"El ID del carrito '{cart_id}' no es válido"
                })
            }

        body = event.get('body')
        if not body:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "El cuerpo de la petición es obligatorio"
                })
            }

        data = json.loads(body)
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        if not product_id or not quantity or quantity <= 0:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Se requiere el 'product_id' y una 'quantity' válida mayor que cero."
                })
            }

        if not ObjectId.is_valid(product_id):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": f"El ID del producto '{product_id}' no es válido."
                })
            }

        cart = carts_collection.find_one({"_id": ObjectId(cart_id)})
        if not cart:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "message": f"No se encontró el carrito con el ID '{cart_id}'"
                })
            }

        product = products_collection.find_one({"_id": ObjectId(product_id)})
        if not product:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "message": f"No se encontró el producto con el ID '{product_id}'"
                })
            }

        product_price = product.get('price')
        if not product_price:
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "message": f"No se pudo obtener el precio del producto con el ID '{product_id}'"
                })
            }

        total = cart.get('total', 0)
        total += product_price * quantity
        cart['total'] = total

        product_data = {
            "id": str(product['_id']),
            "name": product.get('name'),
            "price": product_price,
            "quantity": quantity
        }

        cart_products = cart.get('products', [])
        cart_products.append(product_data)
        cart['products'] = cart_products

        carts_collection.update_one({"_id": ObjectId(cart_id)}, {"$set": cart})

        cart['_id'] = str(cart['_id'])
        cart['user'] = str(cart['user'])

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Producto agregado al carrito de compras exitosamente",
                "cart": cart
            }, indent=2)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": str(e)
            })
        }
