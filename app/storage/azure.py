import logging
import os
from datetime import datetime, timedelta

from azure.storage.blob import (
    AccessPolicy,
    BlobServiceClient,
    ContainerSasPermissions,
    PublicAccess,
)

from app import config

logger = logging.getLogger(__name__)


class AzureStorage:
    client = None
    container_name = ""

    def init(
        self,
        connection_string: str = config.AZURE_STORAGE_CONNECTION_STRING,
        container_name: str = config.AZURE_STORAGE_CONTAINER_NAME,
    ) -> None:
        self.container_name = container_name
        self.client: BlobServiceClient = BlobServiceClient.from_connection_string(
            connection_string
        )

        self.container_client = self.client.get_container_client(self.container_name)

        if not self.container_client.exists():
            self.container_client.create_container()

        access_policy = AccessPolicy(
            permission=ContainerSasPermissions(read=True, write=True),
            expiry=None,
            start=datetime.utcnow() - timedelta(minutes=1),
        )
        identifiers = {"read": access_policy}
        public_access = PublicAccess.CONTAINER

        self.container_client.set_container_access_policy(identifiers, public_access)

    def upload_file(self, file: str) -> str:
        blob = os.path.basename(file)
        blob_client = self.client.get_blob_client(
            container=self.container_name, blob=blob
        )

        with open(file, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        return blob_client.url


azure_storage = AzureStorage()
