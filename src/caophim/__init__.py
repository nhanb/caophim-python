"""Django's command-line utility for administrative tasks."""
import os

from caophim.conf import config


def manage():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "caophim.settings")
    config.django_manage()


def generate_config():
    print(config.generate_json(DEBUG=True))
