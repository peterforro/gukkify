#Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
import boto3

bucket_name = 'gukkify69'
aws_access_key_id = "AKIAJIXDUF3SP2VZ5LUA"
aws_secret_access_key = "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"

s3 = boto3.client(  's3',
                    aws_access_key_id = aws_access_key_id,
                    aws_secret_access_key = aws_secret_access_key   )



def s3_upload(file, acl="public-read"):
    try:
        ExtraArgs = {"ACL":acl, "ContentType":file.content_type}
        s3.upload_fileobj(file,bucket_name,file.filename,ExtraArgs=ExtraArgs)
    except Exception as error:
        print('Upload Error: ', error)
        return error



# def s3_generate_url(files):
#     for file in files:
#         params = {'Bucket':bucket_name, 'Key':file['filename']}
#         file['url'] = s3.generate_presigned_url(ClientMethod='get_object',Params= params)



def s3_generate_url(filename):
        params = {'Bucket':bucket_name, 'Key':filename}
        return s3.generate_presigned_url(ClientMethod='get_object',Params= params)



def s3_delete_file(filename):
    s3.delete_object(Bucket=bucket_name, Key=filename)




#
# s3.create_bucket(
#     ACL='public-read-write',
#     Bucket='xmas',
#     CreateBucketConfiguration={
#         'LocationConstraint': "EU"
#     }
#     # GrantFullControl='string',
#     # GrantRead='string',
#     # GrantReadACP='string',
#     # GrantWrite='string',
#     # GrantWriteACP='string',
#     # ObjectLockEnabledForBucket=True|False
# )
#
