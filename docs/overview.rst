Overview
========

:mod:`pfore-cloud-utilities` is a general functionality library to ease and
abstract some of the frequently used method when developing locally
while interacting with cloud environments, this include Databricks_ and Azure_.

Most of the method requires authentification, refer to the
:doc:`./authentification.rst` section for details on how to set it up.

Assuming that you'll also want to use the package functions while running
spark code remotely on databricks, refer to the
:doc:`./setting_databricks_connect.rst` page to see how
to set up databricks-connect_.

.. _Databricks: https://www.databricks.com
.. _Azure: https://portal.azure.com/#home
.. _databricks-connect: https://learn.microsoft.com/en-us/azure/databricks/dev-tools/databricks-connect-legacy