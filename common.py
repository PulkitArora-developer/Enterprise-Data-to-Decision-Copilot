import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def boto3_clients(service, region):

    # sts_client = boto3.client('sts',
    #                       aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    #                       aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    #                       )
    # resp = sts_client.get_session_token()
    #
    # key = resp['Credentials']['AccessKeyId']
    # secret = resp['Credentials']['SecretAccessKey']
    # session_token = resp['Credentials']['SessionToken']

    return boto3.client(service, region_name=region,
                        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
                        aws_session_token=os.environ.get('AWS_SESSION_TOKEN'))