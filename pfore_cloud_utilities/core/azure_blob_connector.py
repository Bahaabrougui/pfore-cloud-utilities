import io

from azure.core.exceptions import ResourceExistsError
from azure.identity import ClientSecretCredential
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient
from azure.storage.blob import BlobServiceClient

from .singleton import Singleton


class AzureBlobConnector(metaclass=Singleton):
    """Singleton class to interact with an Azure Blob Storage container.

    The classes handle connection, reads and writes inside the container.

    Connection is created using either a Managed Identity or an SPN.

    Upon instantiation, if azure_tenant_id, spn_client_id and spn_client_secret
    are all set to None, the client will assume Managed Identity
    as an authentication method.

    Args:
        account_url: Storage Account url, required
        azure_tenant_id: Azure tenant ID
        spn_client_id: Service Principal client ID
        spn_client_secret: Service Principal client secret

    Raises:
        ValueError: If one of the arguments for SPN-based auth is missing

    """
    def __init__(
            self,
            account_url: str,
            azure_tenant_id: str = None,
            spn_client_id: str = None,
            spn_client_secret: str = None,
            ) -> None:

        # account_url is saved as class attribute to be used for comparison
        # during class instance creation
        self._account_url = account_url

        if (spn_client_id is None and spn_client_secret is None
                and azure_tenant_id is None):
            credentials = DefaultAzureCredential()
        else:
            if None in (azure_tenant_id, spn_client_secret, spn_client_secret):
                raise ValueError(
                    'One of the required arguments for SPN-based '
                    'authentication is not specified. Please either '
                    'specify all required arguments for SPN-based auth, '
                    'or don\'t specify any argument at all for MI-based auth.'
                )
            credentials = ClientSecretCredential(
                tenant_id=azure_tenant_id,
                client_id=spn_client_id,
                client_secret=spn_client_secret,
            )
        self._blob_service_client = BlobServiceClient(
            account_url=self._account_url,
            credential=credentials,
            logging_enable=True,
        )

    def upload(self, contents: bytes, container_name: str, path: str) -> None:
        """Uploads content in bytes to a blob container.

        Args:
            contents: Contents to upload, in bytes
            container_name: Name of the blob container, if it doesn't
                exist it will be created as long as permission scope allows it
            path: Path to write to

        """
        blob_client = self._get_blob_client(container_name, path)
        blob_client.upload_blob(contents, overwrite=True)

    def download(
            self,
            container_name: str,
            path: str,
    ) -> bytes:
        """Downloads content from blob storage.

        Args:
            container_name: Name of the blob container
            path: Path to file

        Returns:
            Blob content in bytes

        """
        blob_client = self._get_blob_client(container_name, path)
        stream = blob_client.download_blob()
        with io.BytesIO() as bytes_io_obj:
            stream.readinto(bytes_io_obj)
            bytes_io_obj.seek(0)
            return bytes_io_obj.read()

    def _get_blob_client(self, container_name: str, file: str) -> BlobClient:
        """Returns blob client to interact with blob inside a container.

        If the specified container's name doesn't exist, it is first created.

        Args:
            container_name: Name of the Blob container
            file: File path of the Blob

        Returns:
            Blob client used to interact with the Blob

        """
        try:
            container_client = self._blob_service_client.create_container(
                name=container_name
            )
        except ResourceExistsError:
            container_client = self._blob_service_client.get_container_client(
                container=container_name
            )

        return container_client.get_blob_client(file)
