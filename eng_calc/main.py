#!/usr/bin/env python3
"""
Application entry point for Engineering Calculator.

Run this module to start the graphical user interface:

    python -m eng_calc.main

Or directly:

    python eng_calc/main.py
"""

import sys


def main() -> int:
    """
    Main entry point for the Engineering Calculator application.

    Returns:
        Exit code from the application.
    """
    from eng_calc.app import create_app

    app = create_app()
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
