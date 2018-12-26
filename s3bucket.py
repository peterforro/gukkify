#Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
import boto3

bucket_name = 'gukkify69'

s3 = boto3.client('s3')
print('S3 connection: ',s3)


def s3_upload(file, acl="public-read"):
    try:
        ExtraArgs = {"ACL":acl, "ContentType":file.content_type}
        s3.upload_fileobj(file,bucket_name,file.filename,ExtraArgs=ExtraArgs)
        print('AWS S3 Upload Successful')
    except Exception:
        print('AWS S3 Upload Error!')



def s3_generate_url(filename):
        params = {'Bucket':bucket_name, 'Key':filename}
        return s3.generate_presigned_url(ClientMethod='get_object',Params= params)



def s3_delete_file(filename):
    s3.delete_object(Bucket=bucket_name, Key=filename)
