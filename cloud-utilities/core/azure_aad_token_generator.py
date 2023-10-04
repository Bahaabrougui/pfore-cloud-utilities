import datetime

from azure.identity import DefaultAzureCredential, ClientSecretCredential

from .singleton import Singleton

aad_resource_name_id_dict = {
    'databricks': '2ff814a6-3304-4ab8-85cb-cd0e6f879c1d',
}


class AADTokenGenerator(metaclass=Singleton):
    """Singleton class to handle AAD token generation of AAD resources."""

    def __init__(
            self,
            spn_client_id: str = None,
            spn_client_secret: str = None,
            azure_tenant_id: str = 'd04f4717-5a6e-4b98-b3f9-6918e0385f4c',
            ) -> None:
        """Creates a connection toward the resource using either a managed
        identity or an SPN.
        If spn_client_id or spn_client_secret are set to None, the client
        will assume Managed Identity as an authentification method.

        :arg spn_client_id: Service Principal client ID
        :arg spn_client_secret: Service Principal client secret
        :arg azure_tenant_id: Azure tenant ID
        """
        if spn_client_id is None or spn_client_secret is None:
            self._credentials = DefaultAzureCredential()
        else:
            self._credentials = ClientSecretCredential(
                tenant_id=azure_tenant_id,
                client_id=spn_client_id,
                client_secret=spn_client_secret,
            )
        self._token = dict()

    def get_token(self, aad_resource_name: str) -> str:
        """Helper method that uses `_credentials` variables
        to make call to the AAD API to generate token
        using Managed Identities.

        :arg: aad_resource_name: AAD resource name

        :returns: AAD token, valid for 60 minutes.
        """
        if aad_resource_name not in aad_resource_name_id_dict.keys():
            raise ValueError('Please specify a valid AAD resource name.')

        # AAD token is only valid for 1 hour
        if not (aad_resource_name in self._token.keys()) or (
            (datetime.datetime.now() -
             self._token[aad_resource_name]['date']).seconds // 60 >= 58
        ):
            self._token[aad_resource_name] = dict()
            self._token[aad_resource_name]['date'] = datetime.datetime.now()
            self._token[aad_resource_name][
                'token'
            ] = self._credentials.get_token(
                f"{aad_resource_name_id_dict[aad_resource_name]}/.default"
            ).token

        return self._token[aad_resource_name]['token']
