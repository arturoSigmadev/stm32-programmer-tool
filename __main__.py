"""
Make package directly executable
Usage: python -m utils.stm32Programmer [command] [options]
"""

from .cli.flash_cli import main

if __name__ == "__main__":
    main()
