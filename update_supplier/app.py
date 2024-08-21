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

        supplier_id = event.get('pathParameters', {}).get('id')
        if not supplier_id:
            return {
                "statusCode": 400,
                "headers": headers_open,
                "body": json.dumps({
                    "message": "El ID del proveedor es requerido en la ruta de la URL"
                })
            }

        if not ObjectId.is_valid(supplier_id):
            return {
                "statusCode": 400,
                "headers": headers_open,
                "body": json.dumps({
                    "message": f"'{supplier_id}' no es un ObjectId válido. Debe ser una cadena hexadecimal de 24 caracteres."
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
        contact = data.get('contact')
        phone = data.get('phone')

        if not any([name, contact, phone]):
            return {
                "statusCode": 400,
                "headers": headers_open,
                "body": json.dumps({
                    "message": "Al menos un campo (name, contact, phone) es requerido para la actualización"
                })
            }

        update_fields = {}
        if name:
            update_fields['name'] = name
        if contact:
            update_fields['contact'] = contact
        if phone:
            update_fields['phone'] = phone

        result = collection.update_one(
            {"_id": ObjectId(supplier_id)},
            {"$set": update_fields}
        )

        if result.modified_count > 0:
            return {
                "statusCode": 200,
                "headers": headers_open,
                "body": json.dumps({
                    "message": "Proveedor actualizado correctamente",
                    "updated_fields": update_fields
                }, indent=2)
            }
        else:
            return {
                "statusCode": 404,
                "headers": headers_open,
                "body": json.dumps({
                    "message": "No se encontró el proveedor con el ID proporcionado o no hubo cambios en la actualización"
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
