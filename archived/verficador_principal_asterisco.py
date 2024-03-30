import boto3,json
#https://unaaldia.hispasec.com/2023/03/ataques-de-ransomware-en-amazon-s3.html
def check_bucket_permissions(bucket_name):
    s3 = boto3.client('s3')
    
    try:
        # Obtener la política de cubo
        bucket_policy = s3.get_bucket_policy(Bucket=bucket_name)
        # Verificar si hay políticas que permitan acceso público
        print("iniciando la comprobacion de las politicas")
        print("//////")
        print("//////")
        print("//////")
        #print(bucket_policy)
        
        print(bucket_policy)
        bucket_policy = json.loads(bucket_policy['Policy'])
        if 'Statement' in bucket_policy:
            for statement in bucket_policy['Statement']:
                if 'Principal' in statement:
                    # Verificar si el acceso es público
                    if statement['Principal'] == '*':
                        print(f"¡El bucket {bucket_name} tiene políticas de acceso público!")
                        return
        print(f"El bucket {bucket_name} no tiene políticas de acceso público.")
    except Exception as e:
        print(f"No se pudo verificar el bucket {bucket_name}: {e}")

def list_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    for bucket in response['Buckets']:
        bucket_name = bucket['Name']
        print(f"Verificando permisos para el bucket: {bucket_name}")
        check_bucket_permissions(bucket_name)

if __name__ == "__main__":
    list_buckets()
