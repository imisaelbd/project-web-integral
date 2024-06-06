import json
from pymongo import MongoClient

client = MongoClient('mongodb+srv://misaelbd:Kk6n.c27JN.RSLK@mongodb-mbd.fqz75ib.mongodb.net/?retryWrites=true&w=majority&appName=MongoDB-MBD')


def lambda_handler(event, __):
    try:
        db = client['project-web-integral']
        collection = db['products']

        products = list(collection.find({}))

        for product in products:
            product['_id'] = str(product['_id'])
            product['supplier'] = str(product['supplier'])

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Productos encontrados",
                "products": products
            }, indent=2)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": str(e)
            })
        }