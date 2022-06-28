# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8

import logging
import os


class MainApp:
    def __init__(self):
        self.is_run = False
        self.appname = os.environ.get("APPNAME")
        self.logger = logging.getLogger(self.appname)
        self.module_name = "mainapp"
        self.logger.info(f"{self.module_name} init successful")

    def __del__(self):
        self.logger.info("exit from application")

    def show_serial_port_list(self):
        pass

    def run(self):
        pass
        self.logger.debug("Do Dispatch")

        self.logger.debug("Dispatch done")

    def exec(self):
        pass
        self.is_run = True
        self.logger.debug("exec")
        while self.is_run:
            pass

        self.logger.debug("exec done")

    def exit(self):
        self.is_run = False
