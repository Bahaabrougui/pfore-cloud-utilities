Authentication
==============

:class:`pfore-cloud-utilities.AzureAADTokenGenerator` and
:class:`pfore-cloud-utilities.AzureBlobConnector` requires authentifcation to function
properly. The authentification can be done either using a managed identity
(case you're running the package form a K8s cluster or whatever resource that
supports AAD MI, or can be done using Service Principals. Authentification
using personal account isn't recommended and therefore wasn't implemented.

To authenticate with a Managed Identity, simply call the class and its methods,
no further configuration is required.
To authenticate using SPNs, you can either hard-code them upon classes
instantiation (highly discouraged), use env variables (also discouraged) or
fetch them securely from a keyvault. To see how to fetch credentials securely,
refer to :doc:`./fetching_secrets.rst`