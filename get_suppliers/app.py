import json
from pymongo import MongoClient

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

        suppliers = list(collection.find({}))

        for supplier in suppliers:
            supplier['_id'] = str(supplier['_id'])

        return {
            "statusCode": 200,
            "headers": headers_open,
            "body": json.dumps({
                "message": "Proveedores encontrados",
                "suppliers": suppliers
            }, indent=2)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers_open,
            "body": json.dumps({
                "message": str(e)
            })
        }