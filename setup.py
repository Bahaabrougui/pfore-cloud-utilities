import os

from setuptools import setup

# If build workflow is triggered from ADO, ARTIFACT_LABEL exists
try:
    setup(
        version=os.environ['ARTIFACT_LABEL']
    )
# If build is triggered for gitHub, use setuptools_scm to fetch tag as version
except KeyError:
    pass
