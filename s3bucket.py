#Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
import boto3

bucket_name = 'gukkify69'


def s3_connection():
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        print('AWS S3 bucket: connected successfully!')
        return s3,bucket
    except Exception:
        print('AWS S3 Bucket: connection failed!')



def s3_get_all_objs(bucket_name):
    bucket = s3_connection()[1]
    objs = bucket.objects.all()
    for i,obj in enumerate(objs):
        print(f"{i+1}){obj.key} - {obj.last_modified}")
    return objs



def s3_upload_file(file):
    bucket = s3_connection()[1]
    try:
        bucket.Object(file.filename).put(Body=file)
        print(f'AWS S3 Bucket - File Upload Succeeded!: {file}')
    except Exception:
        print(f'AWS S3 Bucket - File Upload Failed!: {file}')



def s3_delete_file(filename):
    bucket = s3_connection()[1]
    try:
        bucket.Object(filename).delete()
        print(f'AWS S3 Bucket - File Delete Succeeded!: {filename}')
    except Exception:
        print(f'AWS S3 Bucket - File Delete Failed!: {filename}')


