from capsula.__init__ import s3_client
from capsula import settings


def upload_file(path, file):
    s3_client.put_object(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=path,
        Body=file
    )
