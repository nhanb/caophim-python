"""Django's command-line utility for administrative tasks."""
import os
import sys


def manage():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "caophim.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
