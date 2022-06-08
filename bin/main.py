# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8

import os
import sys
from pathlib import Path

from mainapp import MainApp

def runapp():
    try:
        cwd = Path(os.getcwd())
        approotdir = cwd.parent.absolute()
        app = MainApp(approotdir)
        app.init()
        app.do_dispatch()
    except Exception as ex:
        print(f"Fatal error: {ex}")
        sys.exit(1)

def main():
    runapp()


if __name__ == '__main__':
    main()
