import json
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb+srv://misaelbd:Kk6n.c27JN.RSLK@mongodb-mbd.fqz75ib.mongodb.net/?retryWrites=true&w=majority&appName=MongoDB-MBD')


def lambda_handler(event, __):
    try:
        db = client['project-web-integral']
        collection = db['users']

        user_id = event.get('pathParameters', {}).get('id')
        if not user_id:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "El ID del usuario es requerido en la ruta de la URL"
                })
            }

        if not ObjectId.is_valid(user_id):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": f"'{user_id}' no es un ObjectId válido. Debe ser una cadena hexadecimal de 24 caracteres."
                })
            }

        body = event.get('body')
        if not body:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "El cuerpo de la petición es requerido"
                })
            }

        data = json.loads(body)
        fullname = data.get('fullname')
        username = data.get('user')
        password = data.get('password')

        if not any([fullname, username, password]):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Al menos un campo (fullname, user, password) es requerido para la actualización"
                })
            }

        update_fields = {}
        if fullname:
            update_fields['fullname'] = fullname
        if username:
            update_fields['user'] = username
        if password:
            update_fields['password'] = password

        result = collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_fields}
        )

        if result.modified_count > 0:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Usuario actualizado correctamente",
                    "updated_fields": update_fields
                }, indent=2)
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "message": "No se encontró el usuario con el ID proporcionado o no hubo cambios en la actualización"
                })
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": str(e)
            })
        }
