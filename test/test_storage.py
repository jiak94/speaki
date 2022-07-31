import unittest
from app import config
from app.storage.azure import azure_storage
import os


class TestAzureBlob(unittest.TestCase):
    def setUp(self) -> None:
        azure_storage.init(config.AZURE_BLOB_CONNECTION_STRING, "test1")
        return super().setUp()

    def test_azure_blob(self):
        f = open("./hello_world.txt", "w")
        f.write("Hello World!")
        f.close()

        file = os.path.join("./", "hello_world.txt")
        azure_storage.upload_file(file)

        os.remove(file)
