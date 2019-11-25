from math import radians, cos, sin, asin, sqrt
import base64
import re
import io

from rest_framework.authtoken.models import Token

from capsula.__init__ import s3_client
from capsula.settings import production as settings
from library.models import BookItem
from user.models import User


def upload_file(path, b64file):
    b64file = re.sub('^data:image/.+;base64,', '', b64file) #deleting content-type prefix
    image = io.BytesIO(base64.b64decode(b64file))
    s3_client.put_object(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=path,
        Body=image,
        ACL='public-read'
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


def delete_file(file_path):
    s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_path)


def complete_headers(view_func: object) -> object:
    def wrapped_view(*args, **kwargs):
        response = view_func(*args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    return wrapped_view

def get_books(books):
    data = []
    for book in books:
        item = {}
        item['title'] = book.title
        item['authors'] = book.authors
        item['genre'] = book.genre
        item['id'] = book.id
        data.append({'book': item, 'image': BookItem.objects.filter(book=book)[0].image})
    return data

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371 * c
    return km