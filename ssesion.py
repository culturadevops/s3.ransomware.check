import boto3
from botocore import UNSIGNED
from botocore.config import Config
from botocore import UNSIGNED

from botocore.exceptions import ClientError
from botocore.exceptions import ProfileNotFound
class sessionS3:
    def __init__(self,profile):
        signature_version = UNSIGNED
        try:
            if profile=="":
                self.s3_client = boto3.client("s3", config=Config(signature_version=signature_version))
            else:
                session = boto3.session.Session(profile_name=profile)
                self.s3_client = session.client('s3')
        except ProfileNotFound as error:
            print(f'Did not find the specified AWS CLI profile: {profile}\n')

    def listObjects(self,bucketName):
        try: 
            response = self.s3_client.list_objects(Bucket=bucketName)
            #print(f"getSessionWithoutSession si hubo acceso {bucketName}")
            return "Exitoso",response
        except Exception as e:
            print(f"getSessionWithoutSession No hay acceso a el bucket {bucketName}")
            return "Fallido",None

    def GetBucketPolicy(self,bucketName):
        try: 
            response = self.s3_client.get_bucket_policy(Bucket=bucketName)
            #print(f"getSessionWithoutSession si hubo acceso {bucketName}")
            return "Exitoso",response
        except Exception as e:
            print(f"Error en {bucketName}= {e}")
            return "Fallido",None

    def GetBucketAcl(self,bucketName):
        try: 
            response = self.s3_client.get_bucket_acl(Bucket=bucketName)
            #print(f"getSessionWithoutSession si hubo acceso {bucketName}")
            return response
        except Exception as e:
            print(f"Error {e}")
            return None

    def GetBucketEncryption(self,bucketName):
        try: 
            response = self.s3_client.get_bucket_encryption(Bucket=bucketName)
            #print(f"getSessionWithoutSession si hubo acceso {bucketName}")
            return response
        except Exception as e:
            print(f"Error {e}")
            return None
    def GetBucketVersioning(self,bucketName):
        try: 
            response = self.s3_client.get_bucket_versioning(Bucket=bucketName)
            #print(f"getSessionWithoutSession si hubo acceso {bucketName}")
            versioning = response.get('Status', 'Disabled')
            mfa_delete = response.get('MFADelete', 'Disabled')
            return versioning,mfa_delete
        except Exception as e:
            print(f"Error {e}")
            return "",""
        

    def GetAllBucket(self):
        try:
            target_buckets=[]
            listed_buckets = self.s3_client.list_buckets()
            for bucket in listed_buckets.get('Buckets', []):            
                target_buckets.append(bucket['Name'])
            return target_buckets
        except ClientError as error:
            print(f"Error al intentar acceder al bucket bucket['Name']: ")
            print(f' Failed to list S3 buckets in the current account ({error.response["Error"]["Code"]}): {error.response["Error"]["Message"]}')
            return target_buckets