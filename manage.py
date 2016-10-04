#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'visitorManagement'))

    sys.path.append(ROOT_DIR)
    sys.path.append(APP_DIR)
    app_basename = os.path.basename(APP_DIR)
    os.environ['DJANGO_SETTINGS_MODULE'] = app_basename + '.settings'
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "visitorManagement.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
