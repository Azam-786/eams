import os
import sys

from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
    sys.argv = [
        "src/manage.py",
        "runserver",
        # "0.0.0.0:8000",
    ]  # You can change host:port here
    execute_from_command_line(sys.argv)
