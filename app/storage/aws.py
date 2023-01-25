import boto3
from app import config
import logging
from botocore.exceptions import ClientError
import pathlib

logger = logging.getLogger(__name__)


class S3Storage:
    client = None
    container_name = ""

    def init(
        self,
        access_key_id: str = config.AWS_ACCESS_KEY_ID,
        secret_access_key: str = config.AWS_SECRET_ACCESS_KEY,
        region_name: str = config.AWS_REGION_NAME,
        container_name: str = config.AWS_S3_CONTAINER_NAME,
    ) -> None:
        self.container_name = container_name
        self.region_name = region_name
        print(f"Init S3 Storage: {access_key_id}, {secret_access_key}, {region_name}, {container_name}")
        self.client  = boto3.client(
            's3',
            region_name=region_name,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
        )

        if not self.bucket_exists(self.container_name):
            self.create_bucket(self.container_name)

    def upload_file(self, file: str) -> str | None:
        try:
            response = self.client.upload_file(file, self.container_name, pathlib.Path(file).stem, ExtraArgs={'ACL': 'public-read'})
        except ClientError as e:
            logger.error(e)
            return None
        return f"https://s3.{self.region_name}.amazonaws.com/{self.container_name}/{pathlib.Path(file).stem}"

    def create_bucket(self, bucket_name: str) -> None:
        try:
            self.client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': self.region_name})
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def bucket_exists(self, bucket_name: str) -> bool:
        try:
            self.client.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                return False
        return True


aws_storage = S3Storage()
