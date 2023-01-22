import os
import httpx
import uuid


def test_azure_blob(azure_storage_service):
    f = open("./hello_world.txt", "w")
    f.write("Hello World!")
    f.close()

    file = os.path.join("./", "hello_world.txt")
    azure_storage_service.upload_file(file)

    os.remove(file)

def test_aws_s3_upload(aws_storage_service):
    uid = uuid.uuid4()
    f = open("./uuid.txt", "w")
    f.write(uid.__str__())
    f.close()

    file = os.path.join("./", "uuid.txt")
    download_url = aws_storage_service.upload_file(file)

    assert download_url is not None

    assert httpx.get(download_url).text == uid.__str__()

    os.remove(file)

def test_aws_s3_create_bucket(aws_storage_service):
    assert aws_storage_service.create_bucket("test.bucket.jiakuan")
    aws_storage_service.client.delete_bucket(Bucket="test.bucket.jiakuan")
