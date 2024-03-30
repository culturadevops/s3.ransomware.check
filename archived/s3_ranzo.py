#!/usr/bin/env python3

import argparse
import sys

from time import time

import boto3
from botocore.config import Config
from botocore import UNSIGNED
from botocore.exceptions import ProfileNotFound
from botocore.exceptions import ClientError


def getSessionWithoutSession(nombre_de_tu_bucket):
    #aws s3api put-bucket-acl --bucket paratodousuario --acl public-read
    signature_version = UNSIGNED
    s3_client = boto3.client("s3", config=Config(signature_version=signature_version))
    #s3_client = boto3.client('s3', config=Config(signature_version='s3v4'))
    try: 
        response = s3_client.list_objects(Bucket=nombre_de_tu_bucket)
        print(f"getSessionWithoutSession si hubo acceso {nombre_de_tu_bucket}")
        return "Exitoso"
    except Exception as e:
        print(f"getSessionWithoutSession No hay acceso a el bucket {nombre_de_tu_bucket}")
    return "Fallido"
    #response = s3_client.get_bucket_acl(Bucket=nombre_de_tu_bucket)

def GetAclWithoutSession(nombre_de_tu_bucket):
    #aws s3api put-bucket-acl --bucket paratodousuario --acl public-read
    signature_version = UNSIGNED
    s3_client = boto3.client("s3", config=Config(signature_version=signature_version))
    #s3_client = boto3.client('s3', config=Config(signature_version='s3v4'))
    try: 
        response = s3_client.get_bucket_policy(Bucket=nombre_de_tu_bucket)
        print(f"GetAclWithoutSession si hubo acceso {nombre_de_tu_bucket}")
        return "Exitoso"
    except Exception as e:
        print(f"GetAclWithoutSession No hay acceso a el bucket {nombre_de_tu_bucket}")
    return "Fallido"
    #response = s3_client.get_bucket_acl(Bucket=nombre_de_tu_bucket)


def SearchWithOtherAccount(nombre_de_tu_bucket,profile):
    #aws s3api put-bucket-acl --bucket paratodousuario --acl public-read
    session = boto3.session.Session(profile_name=profile)
    s3_client = session.client('s3')
    #s3_client = boto3.client('s3', config=Config(signature_version='s3v4'))
    try: 
        response = s3_client.list_objects(Bucket=nombre_de_tu_bucket)
        print(f"SearchWithOtherAccount si hubo acceso con otra cuenta {nombre_de_tu_bucket}")
        return "Exitoso"
    except Exception as e:
        print(f"SearchWithOtherAccount No hay acceso a el bucket {nombre_de_tu_bucket}")
        return "Fallido"
    #response = s3_client.get_bucket_acl(Bucket=nombre_de_tu_bucket)
def SearchACLWithOtherAccount(nombre_de_tu_bucket,profile):
    #aws s3api put-bucket-acl --bucket paratodousuario --acl public-read
    session = boto3.session.Session(profile_name=profile)
    s3_client = session.client('s3')
    #s3_client = boto3.client('s3', config=Config(signature_version='s3v4'))
    try: 
        response = s3_client.get_bucket_policy(Bucket=nombre_de_tu_bucket)
        print("SearchACLWithOtherAccount si hubo acceso con otra cuenta {nombre_de_tu_bucket}")
        return "Exitoso"
    except Exception as e:
        print(f"SearchACLWithOtherAccount No hay acceso a el bucket {nombre_de_tu_bucket}")
        return "Fallido"
    #response = s3_client.get_bucket_acl(Bucket=nombre_de_tu_bucket)
        

def main(args):
    if args.profile is None:
        session = boto3.session.Session()
        print('No AWS CLI profile passed in, choose one below or rerun the script using the -p/--profile argument:')
        profiles = session.available_profiles
        for i in range(0, len(profiles)):
            print(f'[{i}] {profiles[i]}')
        profile_number = int(input('Choose a profile (Ctrl+C to exit): ').strip())
        profile_name = profiles[profile_number]
        session = boto3.session.Session(profile_name=profile_name)
    else:
        try:
            profile_name = args.profile
            session = boto3.session.Session(profile_name=profile_name)
        except ProfileNotFound as error:
            print(f'Did not find the specified AWS CLI profile: {args.profile}\n')

            session = boto3.session.Session()
            quit(f'Profiles that are available: {session.available_profiles}\n')

    client = session.client('s3')

    target_buckets = []
    if args.buckets:
        target_buckets.extend(args.buckets.split(','))
    else:
        print('Finding buckets...')
        #try:
        listed_buckets = client.list_buckets()
        for bucket in listed_buckets.get('Buckets', []):            
            target_buckets.append(bucket['Name'])
        #except ClientError as error:
            #print(f"Error al intentar acceder al bucket bucket['Name']: ")
            #quit(f'    Failed to list S3 buckets in the current account ({error.response["Error"]["Code"]}): {error.response["Error"]["Message"]}')

    if len(target_buckets) < 1:
        quit('No buckets found in the target list.')

    print(f'Checking configuration of {len(target_buckets)} buckets...')

    csv_rows = [['Bucket Name',"Acceso sin cuenta","acl sin cuenta",'acceso con cuenta de aws no autorizada',"acl con cuenta no autorizada",'Everyone Read Object','Everyone Read Acl','AuthenticatedUsers Read','AuthenticatedUsers Read Acl','LogDelivery_Read_Acl', 'Object Versioning', 'MFA Delete', 'Note', 'Recommendation']]

    for bucket in target_buckets:
        try:
            Read_Object='Disabled'
            Read_Acl='Disabled'
            AuthenticatedUsers_Read='Disabled'
            AuthenticatedUsers_Read_Acl='Disabled'
            LogDelivery=''
            response = client.get_bucket_acl(Bucket=bucket)
            print("Permisos del bucket:")
            for grant in response['Grants']:
               
                grantee = grant['Grantee']
                permission = grant['Permission']
                print(f"Tipo: {grantee['Type']}, Permiso: {permission}")
                if grant['Permission']=='READ' and grant['Grantee']['Type'] == 'Group' and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
                    Read_Object='Enabled'
                if grant['Permission']=='READ_ACP' and grant['Grantee']['Type'] == 'Group' and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
                    Read_Acl='Enabled'
                if grant['Permission']=='READ' and grant['Grantee']['Type'] == 'Group' and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AuthenticatedUsers':
                    AuthenticatedUsers_Read='Enabled'
                if grant['Permission']=='READ_ACP' and grant['Grantee']['Type'] == 'Group' and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AuthenticatedUsers':
                    AuthenticatedUsers_Read_Acl='Enabled'
                if grant['Permission']=='READ_ACP' and grant['Grantee']['Type'] == 'Group' and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/s3/LogDelivery':
                    LogDelivery=LogDelivery+ " "+'READ_ACP'
                if grant['Permission']=='WRITE_ACP' and grant['Grantee']['Type'] == 'Group' and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/s3/LogDelivery':
                    LogDelivery=LogDelivery+ " "+'WRITE_ACP'
                if grant['Permission']=='READ' and grant['Grantee']['Type'] == 'Group' and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/s3/LogDelivery':
                    LogDelivery=LogDelivery+ " "+'OBJ_READ'
                if grant['Permission']=='WRITE' and grant['Grantee']['Type'] == 'Group' and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/s3/LogDelivery':
                    LogDelivery=LogDelivery+ " "+'OBJ_WRITE'
                if grant['Permission']=='FULL_CONTROL' and grant['Grantee']['Type'] == 'Group' and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/s3/LogDelivery':
                    LogDelivery=LogDelivery+ " "+'FULL_CONTROL'
            if Read_Object!='Enabled':
                unsigned_read=getSessionWithoutSession(bucket)
                otheraccount=SearchWithOtherAccount(bucket,"defaultdebug")
                #
                AclWithoutSession= GetAclWithoutSession(bucket)
                AclWithSession= SearchACLWithOtherAccount(bucket,"defaultdebug")
                #tiene_acl_publica = any(grant['Grantee']['Type'] == 'Group' and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers' for grant in response['Grants'])
            
            #response = client.get_bucket_policy(Bucket=bucket)
            #print("Política de Bucket:")
            #print(response)    
#//.get('Policy')
            response = client.get_bucket_encryption(Bucket=bucket)
            print("Configuración de Transferencia Segura:")
            print(response.get('ServerSideEncryptionConfiguration'))
            print("//////////////////////////")    
            response = client.get_bucket_versioning(Bucket=bucket)
            versioning = response.get('Status', 'Disabled')
            mfa_delete = response.get('MFADelete', 'Disabled')

            #if args.enable_versioning:
            #    if versioning in ['Disabled', 'Suspended']:
            #        try:
            #            client.put_bucket_versioning(
            #                Bucket=bucket,
            #                VersioningConfiguration={
            #                    'Status': 'Enabled',
            #                    'MFADelete': 'Disabled'
            #                }
            #            )
            #            versioning = 'Enabled'
            #            print(f'    Enabled Object Versioning on bucket {bucket}')
            #        except ClientError as error:
            #            print(f'    {error.response["Error"]["Code"]} error running s3:PutBucketVersioning on bucket {bucket}: {error.response["Error"]["Message"]}')

            if versioning == 'Enabled' and mfa_delete == 'Enabled':
                csv_rows.append([
                    bucket,
                    unsigned_read,
                    AclWithoutSession,
                    otheraccount,
                    AclWithSession,
                    Read_Object,
                    Read_Acl,
                    AuthenticatedUsers_Read,
                    AuthenticatedUsers_Read_Acl,
                    LogDelivery,
                    versioning,
                    mfa_delete,
                    'Bucket is protected against ransomware attacks',
                    'None'
                ])
            elif versioning == 'Enabled' and mfa_delete != 'Enabled':
                csv_rows.append([
                    bucket,
                    unsigned_read,
                    AclWithoutSession,
                    otheraccount,
                    AclWithSession,
                    Read_Object,
                    Read_Acl,
                    AuthenticatedUsers_Read,
                    AuthenticatedUsers_Read_Acl,
                    LogDelivery,
                    versioning,
                    mfa_delete,
                    '"Bucket is protected against ransomware attacks, but an attacker may make the bucket vulnerable by disabling object versioning with the s3:PutBucketVersioning permission"',
                    'Enable MFA delete'
                ])
            else:
                csv_rows.append([
                    bucket,
                    unsigned_read,
                    AclWithoutSession,
                    otheraccount,
                    AclWithSession,
                    Read_Object,
                    Read_Acl,
                    AuthenticatedUsers_Read,
                    AuthenticatedUsers_Read_Acl,
                    LogDelivery,                    
                    versioning,
                    mfa_delete,
                    'Bucket is VULNERABLE to ransomware attacks',
                    'Enable object versioning and MFA delete'
                ])
        except ClientError as error:
            print(f'    {error.response["Error"]["Code"]} error running s3:GetBucketVersioning on bucket {bucket}: {error.response["Error"]["Message"]}')
            # Continue on anyways, doesn't mean every bucket will fail

    csv_file_name = f'{profile_name}_ransomware_bucket_scan_{str(time()).split(".")[0]}.csv'

    if len(csv_rows) > 1:
        with open(f'./{csv_file_name}', 'w+') as f:
            for row in csv_rows:
                f.write(','.join(row) + '\n')
        print(f'\nScan complete, successful results output to ./{csv_file_name}')
    else:
        print('\nScan complete, no successful results to output though...')


def quit(err_msg, err_code=1):
    print(err_msg)
    print('\nQuitting...')
    sys.exit(err_code)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This script accepts AWS credentials and scans the target S3 buckets for their object versioning and MFA delete configurations, then outputs the results and a recommendation to a CSV file.')

    parser.add_argument('-p', '--profile', required=False, default=None, help='The AWS CLI profile to use for making API calls. This is usually stored under ~/.aws/credentials. You will be prompted by default.')
    parser.add_argument('-s', '--profileSecundary', required=False, default=None, help='The AWS CLI profile to use for making API calls. This is usually stored under ~/.aws/credentials. You will be prompted by default.')
    parser.add_argument('-b', '--buckets', required=False, default=None, help='A comma-separated list of S3 buckets in the current account to check. By default, all buckets in the account will be checked.')
    args = parser.parse_args()

    main(args)


    