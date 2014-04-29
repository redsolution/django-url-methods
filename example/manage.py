#!/usr/bin/python
import os, sys

example_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(example_dir)

sys.path[0:0] = [
    example_dir,
    parent_dir,
]

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        from django.core.management import execute_manager
        try:
            import settings  # Assumed to be in the same directory.
        except ImportError:
            sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
            sys.exit(1)
        execute_manager(settings)
    else:
        execute_from_command_line(sys.argv)
