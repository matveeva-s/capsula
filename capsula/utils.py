import base64

from rest_framework.authtoken.models import Token
from botocore.exceptions import ClientError

from capsula.__init__ import s3_client
from capsula import settings
from user.models import User


def upload_file(path, file):
    s3_client.put_object(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=path,
        Body=file
    )


def download_file(path):
    s3_response_object = s3_client.get_object(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=path)
    object_content = s3_response_object['Body'].read()
    return object_content


def get_user_from_request(request):
    token = request.headers['Authorization'][6:]
    django_user = Token.objects.get(key=token).user
    user = User.objects.get(django_user=django_user)
    return user


def check_key_existing(key):
    try:
        s3_client.head_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
    except ClientError as e:
        return False
    return True


def get_b64str_from_path(file_path):
    encoded_string = base64.b64encode(download_file(file_path)).decode('utf-8')
    return encoded_string


def delete_file(file_path):
    if check_key_existing(file_path):
        s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_path)
        return True
    else:
        return False
