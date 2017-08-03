import datetime
import os
import boto3

from decouple import config, Csv

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_LOCATION = 'static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = '//%s.s3.amazonaws.com/static/' % AWS_STORAGE_BUCKET_NAME

DEFAULT_FILE_STORAGE = 'whatachore.storage_backends.MediaStorage'
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL


# Gather list of icon names
client = boto3.client('s3',
                     aws_access_key_id=AWS_ACCESS_KEY_ID,
                     aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

files = client.list_objects_v2(Bucket=AWS_STORAGE_BUCKET_NAME, Prefix='static/wac/styles/images/icons/red_icons/')
ICON_NAMES = []
for file in files['Contents']:
    full_key = file['Key']
    stuff_to_remove = 'static/wac/styles/images/icons/red_icons/'
    name = full_key.replace(stuff_to_remove, '')
    ICON_NAMES.append(name)
