import io
from typing import Union

from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.core.exceptions import ResourceExistsError

from .singleton import Singleton


class AzureBlobConnector(metaclass=Singleton):
    """Singleton class to handle connection, reads and write inside an Azure
    Blob Storage container.
    """
    def __init__(
            self,
            account_url: str,
            spn_client_id: str = None,
            spn_client_secret: str = None,
            azure_tenant_id: str = 'd04f4717-5a6e-4b98-b3f9-6918e0385f4c',
            ) -> None:
        """Creates a connection using either a managed identity or an SPN.
        If spn_client_id or spn_client_secret are set to None, the client
        will assume Managed Identity as an authentification method.

        :arg account_url: Storage Account url, required
        :arg spn_client_id: Service Principal client ID
        :arg spn_client_secret: Service Principal client secret
        :arg azure_tenant_id: Azure tenant ID
        """
        # account_url is saved as class attribute to be used for comparison
        # during class instance creation
        self.account_url = account_url
        if spn_client_id is None or spn_client_secret is None:
            credentials = DefaultAzureCredential()
        else:
            credentials = ClientSecretCredential(
                tenant_id=azure_tenant_id,
                client_id=spn_client_id,
                client_secret=spn_client_secret,
            )
        self.blob_service_client = BlobServiceClient(
            account_url=self.account_url,
            credential=credentials,
            logging_enable=True,
        )

    def upload(self, contents: bytes, container_name: str, path: str) -> None:
        """Uploads content in bytes to a blob container.

        :param contents: Contents to upload, in bytes
        :param container_name: Name of the blob container, if it doesn't
            exist it will be created as long as permission scope allows it
        :param path: Path to write to
        """
        blob_client = self._get_blob_client(container_name, path)
        blob_client.upload_blob(contents, overwrite=True)

    def download(
            self,
            container_name: str,
            path: str,
    ) -> bytes:
        """Downloads content from blob storage

        :param container_name: Name of the blob container
        :param path: Path to file
        :return: Blob content in bytes
        """
        blob_client = self._get_blob_client(container_name, path)
        stream = blob_client.download_blob()
        with io.BytesIO() as bytes_io_obj:
            stream.readinto(bytes_io_obj)
            bytes_io_obj.seek(0)
            return bytes_io_obj.read()

    def _get_blob_client(self, container_name: str, file: str) -> BlobClient:
        """Gets blob client to interact with blob inside a container.
        If the specified container's name doesn't exist, it is first created.
        """
        try:
            container_client = self.blob_service_client.create_container(
                name=container_name
            )
        except ResourceExistsError:
            container_client = self.blob_service_client.get_container_client(
                container=container_name
            )

        return container_client.get_blob_client(file)
