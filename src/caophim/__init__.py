import os

from caophim.conf import config


def manage():
    """Django's command-line utility for administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "caophim.settings")
    config.django_manage()  # use goodconf to run a monkey-patched "manage.py"


def generate_config():
    print(config.generate_json(DEBUG=True))


def generate_psql_envars():
    """
    Outputs shell statements to set Postgres connection envars.
    Usage:
        caophim-generate-psql-envars | source
        psql  # or even better, pgcli
        # should drop you into the caophim db shell
    """
    print(
        f"""\
export PGHOST='{config.DB_HOST}'
export PGPORT='{config.DB_PORT}'
export PGDATABASE='{config.DB_NAME}'
export PGUSER='{config.DB_USER}'
export PGPASSWORD='{config.DB_PASSWORD}'
"""
    )
