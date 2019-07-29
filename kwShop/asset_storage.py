from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage): # 이미지 파일 모두 S3에 업로드 되게 설정
    location = 'media'
    file_overwrite = False

