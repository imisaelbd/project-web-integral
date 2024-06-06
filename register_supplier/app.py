import json
from pymongo import MongoClient

client = MongoClient('mongodb+srv://misaelbd:Kk6n.c27JN.RSLK@mongodb-mbd.fqz75ib.mongodb.net/?retryWrites=true&w=majority&appName=MongoDB-MBD')


def lambda_handler(event, __):
    try:
        db = client['project-web-integral']
        collection = db['suppliers']

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
        contact = data.get('contact')
        phone = data.get('phone')

        if not name or not contact or not phone:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Todos los campos son requeridos (nombre, contacto, teléfono)"
                })
            }

        existing_supplier = collection.find_one({"name": name})
        if existing_supplier:
            existing_supplier['_id'] = str(existing_supplier['_id'])
            return {
                "statusCode": 409,
                "body": json.dumps({
                    "message": f"El proveedor '{name}' ya existe en la base de datos",
                    "supplier": existing_supplier
                })
            }

        supplier = {
            'name': name,
            'contact': contact,
            'phone': phone
        }

        result = collection.insert_one(supplier)

        if result.inserted_id:
            supplier['_id'] = str(result.inserted_id)
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Proveedor registrado correctamente",
                    "supplier": supplier
                }, indent=2)
            }
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "message": "Error al insertar el proveedor"
                })
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": str(e)
            })
        }
