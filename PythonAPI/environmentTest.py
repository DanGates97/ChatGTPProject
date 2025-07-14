import sys
import os


def is_in_venv():
    return sys.prefix != getattr(sys, "base_prefix", sys.prefix)


if is_in_venv():
    print("Inside a virtual environment")
else:
    print("Not in a virtual environment")

    
if "VIRTUAL_ENV" in os.environ:
    print("Inside a virtual environment")
else:
    print("Not in a virtual environment")