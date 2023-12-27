# minio_storage.py
from minio import Minio
from minio.error import S3Error
from django.core.files.storage import Storage
from django.conf import settings

class MinioStorage(Storage):
    def __init__(self, *args, **kwargs):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )
        self.bucket_name = settings.MINIO_BUCKET_NAME

        super().__init__()

    def _save(self, name, content):
        try:
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=name,
                data=content,
                length=content.size,
                content_type=content.content_type,
            )
        except S3Error as e:
            raise IOError(str(e))

        return name

    def url(self, name):
        # Generate a public URL for the file
        client = self.client.presigned_get_object(self.bucket_name, name)
        return client.replace("minio:9000", "185.204.2.233:9999").split('?')[0]
    
    def exists(self, name: str) -> bool:
        try:
            self.client.stat_object(self.bucket_name, name)
            return True
        except S3Error as e:
            if e.code == "NoSuchKey":
                return False
            raise
