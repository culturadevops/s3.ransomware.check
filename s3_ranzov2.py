#!/usr/bin/env python3

import argparse
import sys
from time import time
import ssesion

class csv_manager:
    def __init__(self,out,column):
        self.output=out
        self.csv_rows = [column]
    def add(self,rows):
        self.csv_rows.append(rows)
    def writeFile(self):
        csv_file_name = f'{self.output}_ransomware_bucket_scan_{str(time()).split(".")[0]}.csv'
        print(self.csv_rows )
        if len(self.csv_rows) > 1:
            with open(f'./{csv_file_name}', 'w+') as f:
                for row in self.csv_rows:
                    f.write(','.join(row) + '\n')
            print(f'\nScan complete, successful results output to ./{csv_file_name}')
        else:
            print('\nScan complete, no successful results to output though...')

def main(args):

    if args.profile is None:
        quit("Need principal profile")

    if args.profileSecundary is None:
        quit("need Secundary profile")

    if args.profile ==args.profileSecundary:
        quit("principal and secundary profile can not be the same")
       

    principal=ssesion.sessionS3(args.profile)
    secundario=ssesion.sessionS3(args.profileSecundary)
    target_buckets = []
    
    if args.output is None:
        output=args.profile
    else:
        output=args.output
    if args.buckets:
        target_buckets.extend(args.buckets.split(','))
    else:
        print('Finding buckets...')
        print(principal)
        target_buckets = principal.GetAllBucket()   

    if len(target_buckets) < 1:
        quit('No buckets found in the target list.')


    # se declara las variables aqui porque aqui termina la validacion inicial    
    nosession=ssesion.sessionS3("")
    csvfile=csv_manager(output,['Bucket Name',"Acceso sin cuenta","acl sin cuenta",'acceso con cuenta de aws no autorizada',"acl con cuenta no autorizada",'Everyone Read Object','Everyone Read Acl','AuthenticatedUsers Read','AuthenticatedUsers Read Acl','LogDelivery_Read_Acl', 'Object Versioning', 'MFA Delete', 'Note', 'Recommendation'])



    print(f'Checking configuration of {len(target_buckets)} buckets...')
    for bucket in target_buckets:
            Read_Object='Disabled'
            Read_Acl='Disabled'
            AuthenticatedUsers_Read='Disabled'
            AuthenticatedUsers_Read_Acl='Disabled'
            LogDelivery=''
            unsigned_read,x=nosession.listObjects(bucket)
            otheraccount,x=secundario.listObjects(bucket)
            AclWithoutSession,x= nosession.GetBucketPolicy(bucket)
            AclWithSession,x= secundario.GetBucketPolicy(bucket)

            response = principal.GetBucketAcl(bucket)
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

                
            versioning,mfa_delete= principal.GetBucketVersioning(bucket)
            Note=      ""
            Recommendation= ""
            if versioning == 'Enabled' and mfa_delete == 'Enabled':
              Note= 'Bucket is protected against ransomware attacks'
              Recommendation= 'None'
            elif versioning == 'Enabled' and mfa_delete != 'Enabled':
                Note= '"Bucket is protected against ransomware attacks, but an attacker may make the bucket vulnerable by disabling object versioning with the s3:PutBucketVersioning permission"'
                Recommendation= 'Enable MFA delete' 
            else:
                Note= 'Bucket is VULNERABLE to ransomware attacks'
                Recommendation= 'Enable object versioning and MFA delete'
            csvfile.add([
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
                    Note,
                    Recommendation
                ])   
                    
    csvfile.writeFile()

def quit(err_msg, err_code=1):
    print(err_msg)
    print('\nQuitting...')
    sys.exit(err_code)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This script accepts AWS credentials and scans the target S3 buckets for their object versioning and MFA delete configurations, then outputs the results and a recommendation to a CSV file.')
    parser.add_argument('-p', '--profile', required=False, default=None, help='The AWS CLI profile to use for making API calls. This is usually stored under ~/.aws/credentials. You will be prompted by default.')
    parser.add_argument('-b', '--buckets', required=False, default=None, help='A comma-separated list of S3 buckets in the current account to check. By default, all buckets in the account will be checked.')
    parser.add_argument('-s', '--profileSecundary', required=False, default=None, help='The AWS CLI profile to use for making API calls. This is usually stored under ~/.aws/credentials. You will be prompted by default.')
    parser.add_argument('-o', '--output', required=False, default=None, help='The AWS CLI profile to use for making API calls. This is usually stored under ~/.aws/credentials. You will be prompted by default.')
    args = parser.parse_args()
    main(args)


    