
def handler(event, context):
    print("Evento recebido:", event)
    return {"statusCode": 200, "body": "Olá do LocalStack Lambda"}
