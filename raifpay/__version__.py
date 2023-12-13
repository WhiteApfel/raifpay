from os import environ

__version__ = environ.get("TAG_VERSION", "v0.0.0a1").replace("v", "")
