import requests
import io
import itertools
import os
import urllib.parse

import boto3
from PIL import Image, ImageFilter


'''
This is basic function for generating thumbnails
 

'''

# ENVIRONMENT VARIABLES
IMAGE_FOLDER = os.environ.get('IMAGE_FOLDER', "image/")
CALLBACK_URL = os.environ.get('CALLBACK_URL', "http://localhost:8000/async_image_upload/presignedurl/{key}/")
THUMB_DIMENSION_SMALL = int(os.environ.get('THUMB_DIMENSION_SMALL', 50))
THUMB_DIMENSION_MEDIUM = int(os.environ.get('THUMB_DIMENSION_MEDIUM', 100))
THUMB_DIMENSION_LARGE = int(os.environ.get('THUMB_DIMENSION_LARGE', 400))
BLUR = os.environ.get('BLUR', False)
BLUR_RADIUS = int(os.environ.get('BLUR_RADIUS', 20))


# THUMB DIMENSIONS
size_original = None
size_small_square_crop = (THUMB_DIMENSION_SMALL, THUMB_DIMENSION_SMALL)
size_medium_square_crop = (THUMB_DIMENSION_MEDIUM, THUMB_DIMENSION_MEDIUM)
size_large_square_crop = (THUMB_DIMENSION_LARGE, THUMB_DIMENSION_LARGE)

THUMB_SIZES = [size_original,
               size_small_square_crop,
               size_medium_square_crop,
               size_large_square_crop
               ]


# Entry Point
def lambda_handler(event, context):
    print(event)
    # retrive bucket and key from event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')


    try:
        generate_thumbs(bucket, key)
    except Exception as e:
        print(e)
        resp = invoke_callback(key, e)
        return {"error": str(e), "resp": resp.json()}

    resp = invoke_callback(key)
    return {"resp": resp.json()}


def set_new_key(size, blur, key, format):
    # sized:    <IMAGE_FOLDER>/abc_100x100.jpg
    # blurred:  <IMAGE_FOLDER>/abc_100x100_blurred.jpg

    path, path_ext = os.path.splitext(key)
    ext = path_ext if path_ext else f".{format}"
    ext = ext.lower()
    filename = path.split('/')[-1]
    blur_suffix = '_blurred'

    new_key = None

    if size is not None:
        size_suffix = f'_{size[0]}x{size[0]}'
        if blur:
            new_key = f'{IMAGE_FOLDER}{filename}{size_suffix}{blur_suffix}{ext}'
        else:
            new_key = f'{IMAGE_FOLDER}{filename}{size_suffix}.{ext}'
    else:
        if blur:
            new_key = f'{IMAGE_FOLDER}{filename}{blur_suffix}.{ext}'
    return new_key



def generate_thumbs(bucket, key):

    s3 = boto3.client('s3')

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
    except Exception as e:
        print(
            'Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(
                key, bucket))
        raise e

    metadata = response['Metadata']


    blur_radius = BLUR_RADIUS
    size_comb = list(itertools.product(THUMB_SIZES, [True, False])) if BLUR else THUMB_SIZES

    # resize & blur
    file_byte_string = response['Body'].read()
    for size, blur in size_comb:
        pil_image = Image.open(io.BytesIO(file_byte_string))
        in_mem_file = io.BytesIO()

        if size is None:
            if blur:
                pil_image.filter(ImageFilter.GaussianBlur(blur_radius)).save(in_mem_file, format=pil_image.format)
            else:
                pil_image.save(in_mem_file, format=pil_image.format)
        else:
            pil_image.thumbnail(size, Image.ANTIALIAS)
            if blur:
                blur_radius = size[0] / 100
                pil_image.filter(ImageFilter.GaussianBlur(blur_radius)).save(in_mem_file, format=pil_image.format)
            else:
                pil_image.save(in_mem_file, format=pil_image.format)

        content_type = f"{pil_image.get_format_mimetype()}"
        format = pil_image.format
        in_mem_file.seek(0)

        new_key = set_new_key(size, blur, key, format)
        if new_key is not None:
            s3.put_object(Body=in_mem_file,
                          Bucket=bucket,
                          Key=new_key,
                          ContentType=content_type,
                          Metadata=metadata)


def invoke_callback(key, error=None):
    data = {}
    headers = {'content-type': 'application/json'}
    if error:
        data['error'] = repr(error)
    return requests.put(CALLBACK_URL.replace('{key}', key), data=data, headers=headers)

