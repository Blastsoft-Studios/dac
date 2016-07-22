#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dac.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
<<<<<<< HEAD
=======

>>>>>>> da0542e3e26b0e0108fb1218fd0960a2f4e2d9cc
