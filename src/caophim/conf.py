import secrets

from goodconf import GoodConf, Value


class Config(GoodConf):
    DEBUG = Value(default=False)
    SECRET_KEY = Value(initial=lambda: secrets.token_urlsafe(60))
    DB_HOST = Value(default="127.0.0.1")
    DB_PORT = Value(default="5432")
    DB_NAME = Value(default="caophim")
    DB_USER = Value(default="caophim")
    DB_PASSWORD = Value(default="password")

    # AWS creds used for the S3 storage backend for uploaded pics
    AWS_ACCESS_KEY_ID = Value()
    AWS_SECRET_ACCESS_KEY = Value()
    AWS_STORAGE_BUCKET_NAME = Value(default="caophim")
    AWS_DEFAULT_ACL = Value(default="public-read")
    AWS_S3_ENDPOINT_URL = Value(default="")


config = Config(default_files=["caophim.conf.json"])
