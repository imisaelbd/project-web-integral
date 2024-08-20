import json
from pymongo import MongoClient

client = MongoClient('mongodb+srv://misaelbd:Kk6n.c27JN.RSLK@mongodb-mbd.fqz75ib.mongodb.net/?retryWrites=true&w=majority&appName=MongoDB-MBD')


def lambda_handler(event, __):
    try:
        db = client['project-web-integral']
        collection = db['users']

        body = event.get('body')
        if not body:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "El cuerpo en la petición es requerido"
                })
            }

        data = json.loads(body)

        fullname = data.get('fullname')

        user = data.get('user')

        password = data.get('password')


        if not fullname or not user or not password:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Todos los campos son obligatorios (fullname, user, password)"
                })
            }

        existing_user = collection.find_one({"user": user})
        if existing_user:
            existing_user['_id'] = str(existing_user['_id'])
            return {
                "statusCode": 409,
                "body": json.dumps({
                    "message": f"El usuario '{user}' ya existe en la base de datos",
                    "user": existing_user
                })
            }

        user_data = {
            'fullname': fullname,
            'user': user,
            'password': password
        }

        result = collection.insert_one(user_data)

        if result.inserted_id:
            user_data['_id'] = str(result.inserted_id)
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Usuario registrado correctamente",
                    "user": user_data
                }, indent=2)
            }
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "message": "Error al insertar el usuario"
                })
            }

    except Exception as e: 
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": str(e)
            })
        }