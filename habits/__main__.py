"""Punto de entrada para ejecutar la aplicación con `python -m habits`."""

import sys

from habits.cli import main

if __name__ == "__main__":
    sys.exit(main())
