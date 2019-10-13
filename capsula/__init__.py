import boto3
from capsula import settings

s3_session = boto3.session.Session()
s3_client = s3_session.client(
    service_name='s3',
    endpoint_url='https://hb.bizmrg.com/',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
)
