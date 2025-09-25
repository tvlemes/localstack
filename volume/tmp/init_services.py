import boto3
import zipfile
import os

# ========================
# CONFIGURAÇÕES GERAIS
# ========================
LOCALSTACK_URL = "http://localhost:4566"
REGION = "us-east-1"

session = boto3.session.Session(
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name=REGION,
)

# ========================
# 1. S3 - Bucket
# ========================
def create_s3():
    s3 = session.client("s3", endpoint_url=LOCALSTACK_URL)
    bucket_name = "meu-bucket-local"
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"[S3] Bucket criado: {bucket_name}")
    except Exception as e:
        print(f"[S3] Erro: {e}")


# ========================
# 2. DynamoDB - Tabela
# ========================
def create_dynamodb():
    dynamo = session.client("dynamodb", endpoint_url=LOCALSTACK_URL)
    table_name = "Clientes"
    try:
        dynamo.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": "Id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "Id", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        print(f"[DynamoDB] Tabela criada: {table_name}")
    except Exception as e:
        print(f"[DynamoDB] Erro: {e}")


# ========================
# 3. EC2 e VPC
# ========================
def create_vpc():
    ec2 = session.client("ec2", endpoint_url=LOCALSTACK_URL)
    try:
        vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")
        vpc_id = vpc["Vpc"]["VpcId"]
        print(f"[EC2/VPC] VPC criada: {vpc_id}")
    except Exception as e:
        print(f"[EC2/VPC] Erro: {e}")


# ========================
# 4. Lambda
# ========================
def create_lambda():
    lambda_client = session.client("lambda", endpoint_url=LOCALSTACK_URL)

    # Código simples da Lambda
    lambda_code = """
def handler(event, context):
    print("Evento recebido:", event)
    return {"statusCode": 200, "body": "Olá do LocalStack Lambda"}
"""

    os.makedirs("lambda", exist_ok=True)
    with open("lambda/lambda_function.py", "w") as f:
        f.write(lambda_code)

    with zipfile.ZipFile("lambda.zip", "w") as zf:
        zf.write("lambda/lambda_function.py", arcname="lambda_function.py")

    try:
        lambda_client.create_function(
            FunctionName="MinhaLambda",
            Runtime="python3.9",
            Role="arn:aws:iam::000000000000:role/lambda-role",
            Handler="lambda_function.handler",
            Code={"ZipFile": open("lambda.zip", "rb").read()},
        )
        print("[Lambda] Função criada: MinhaLambda")
    except Exception as e:
        print(f"[Lambda] Erro: {e}")


# ========================
# 5. Glue
# ========================
def create_glue():
    glue = session.client("glue", endpoint_url=LOCALSTACK_URL)
    try:
        db_name = "meu_db_glue"
        glue.create_database(DatabaseInput={"Name": db_name})
        print(f"[Glue] Database criado: {db_name}")
    except Exception as e:
        print(f"[Glue] Erro: {e}")


# ========================
# EXECUÇÃO
# ========================
if __name__ == "__main__":
    create_s3()
    # create_dynamodb()
    create_vpc()
    create_lambda()
    # create_glue()
    print("\n✅ Ambiente inicializado no LocalStack")

'''
📌 O que ele faz
Cria bucket S3 chamado meu-bucket-local
Cria tabela DynamoDB chamada Clientes
Cria uma VPC com CIDR 10.0.0.0/16
Cria uma função Lambda simples que retorna JSON
Cria um banco Glue chamado meu_db_glue
'''