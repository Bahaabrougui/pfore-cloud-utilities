# Dynamically get the version of the installed module
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("cloud-utilities")
except PackageNotFoundError:
    # package is not installed
    pass
