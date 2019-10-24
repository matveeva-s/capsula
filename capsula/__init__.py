import os

import boto3
from capsula.settings import production, development

#todo fix
if os.environ['DJANGO_SETTINGS_MODULE'] == 'capsula.settings.production':
    s3_session = boto3.session.Session()
    s3 = boto3.resource('s3')
    s3_bucket = s3.Bucket(production.AWS_STORAGE_BUCKET_NAME)
    s3_client = s3_session.client(
        service_name='s3',
        endpoint_url='https://hb.bizmrg.com/',
        aws_access_key_id=production.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=production.AWS_SECRET_ACCESS_KEY
    )
else:
    s3_session = boto3.session.Session()
    s3 = boto3.resource('s3')
    s3_bucket = s3.Bucket(production.AWS_STORAGE_BUCKET_NAME)
    s3_client = s3_session.client(
        service_name='s3',
        endpoint_url='https://hb.bizmrg.com/',
        aws_access_key_id=development.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=development.AWS_SECRET_ACCESS_KEY
    )