# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
"""
Порядок и условия запуска
Если запустить вайл без параметров, то программа ищет config_file_name определенный в функции main,
Если запустить файл с параметром "-c" то программа пытается запуститься с конфигом указанном в параметре
Если конфиг не удается найти - программа завершает свое выполение.
Если определен параметр запуска devmode=True - то используется путь конфигу определенный разработчиком в функции
Launcher.__load_dev_params
Если определен параметр -d, то программа ипользует rootdir из переданого значения из параметра.
Если параметр -d не определен, то программа ищит ближайшую директорию относительно запуска bin, etc, var. Если из этой
директории доступен etc/{settings.json}, то директория считается rootdir, иначе программа завешается

"""

import argparse
import datetime
import json
import logging
import os
import pathlib
import sys
import time
from pathlib import Path

from lib import jsonconfigutils
from mainapp import MainApp


class Launcher():
    def __init_arg_parser(self):
        self.__parser = argparse.ArgumentParser()
        self.__parser.add_argument("-c", "--config", action='store', dest="config",
                                   help="path to config file name")
        self.__parser.add_argument("-r", "--rootdir", action='store', dest="rootdir",
                                   help="path to applition root directory")

    def __load_dev_params(self):
        myargs = " --config " + self.__config_file_name
        args = self.__parser.parse_args(myargs.split())
        return args

    def __load_args(self):
        if self.__devmode:
            self.args = self.__load_dev_params()
        else:
            self.args = self.__parser.parse_args()

    def __locate_root_dir(self):

        def check_cwd_is_root():
            bin_path = os.path.join(os.getcwd(), "bin")
            etc_path = os.path.join(os.getcwd(), "etc")
            var_path = os.path.join(os.getcwd(), "var")
            if os.path.isdir(bin_path) and os.path.isdir(etc_path) and os.path.isdir(var_path):
                if os.path.isfile( os.path.join(os.getcwd(),"etc", self.__config_file_name)):
                    self.rootdir = os.path.realpath(os.getcwd())

        cwd = str(os.path.realpath(os.getcwd())).split("/")[-1]
        if cwd == "bin":
            os.chdir("../")
        check_cwd_is_root()

    def __init__(self, appname, config_file_name=None, devmode=False):
        self.rootdir = None
        self.appname = appname
        if config_file_name:
            self.__config_file_name = config_file_name
        else:
            self.__config_file_name = f"{appname}.json"
        self.__devmode = devmode
        self.__init_arg_parser()
        self.__load_args()
        self.__locate_root_dir()

    def __read_config(self, configname):
        try:
            print(f"loading config from {os.path.abspath(configname)}")
            with open(configname, 'r') as f:
                config = json.load(f)
            self.__gconfig = config
        except Exception as ex:
            raise Exception(f"loadconfig error: {ex}")

    def __findconfig(self):
        if self.rootdir:
            configfilepath = os.path.join(self.rootdir, "etc", self.__config_file_name)
            if os.path.isfile(configfilepath):
                return configfilepath
        else:
            config_paths = ["./", "etc/", "../etc/", ""]
            file_config_paths = [f"{el}{self.__config_file_name}" for el in config_paths]

            for file_config_path in file_config_paths:
                filepath = os.path.join(os.getcwd(), (file_config_path))
                if os.path.isfile(filepath):
                    return filepath
        return None

    def parse_args(self):
        if self.args.rootdir:
            self.rootdir = self.args.rootdir
        if self.args.config:
            self.cofig = self.args.config
            self.__read_config(self.config)
        else:
            self.config = self.__findconfig()
            if self.config:
                self.__read_config(self.config)
            else:
                raise RuntimeError("Configuration file not found")

    def __init_logger_params(self):
        self.__log_enable = bool(jsonconfigutils.getConfigValue(self.__gconfig, "/settings/logger/main/enable", False))
        if self.__log_enable:
            self.__log_backup_count = jsonconfigutils.getConfigValue(
                self.__gconfig, "/settings/logger/main/backupCount", 33)

            self.__log_enable_debug = bool(jsonconfigutils.getConfigValue(
                self.__gconfig, "/settings/logger/main/enableDebug", False))

            self.__log_detailed = bool(jsonconfigutils.getConfigValue(
                self.__gconfig, "/settings/logger/main/detailedLog", False))

            self.__log_enable_stdout = bool(
                jsonconfigutils.getConfigValue(self.__gconfig, "/settings/logger/stdout", False))

            self.__log_dir = jsonconfigutils.getConfigValue(
                self.__gconfig, "/settings/logger/main/logdir", "var/log/")
        else:
            print("logging is disabled!")

    def __init_file_log_handler(self, formatter):
        if not self.rootdir:
            raise RuntimeError(
                f"can't locate application root directory."
                f"Run this command to read more information {sys.argv[0]} -h")
        filename = f"{self.appname}.log"
        fullpathlogdir = os.path.join(self.rootdir, self.__log_dir, filename)
        rotate_time = datetime.time(hour=0, minute=0, second=0)

        # # create time rotating file handler
        fh = logging.handlers.TimedRotatingFileHandler(
            fullpathlogdir, atTime=rotate_time, backupCount=self.__log_backup_count)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def __init_stream_log_handler(self, formatter):
        # # create console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def __initLogger(self):
        self.logger = logging.getLogger(self.appname)
        if self.__log_enable_debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            u'[%(asctime)s] [%(name)s]# %(levelname)s\t : %(message)s')
        if self.__log_detailed:
            formatter = logging.Formatter(
                u'[%(asctime)s] [FILE:%(filename)s] [LINE:%(lineno)d]# %(levelname)s: %(message)s')

        if self.__log_enable_stdout:
            self.__init_stream_log_handler(formatter)
        self.__init_file_log_handler(formatter)

    def start_logger(self):
        self.__init_logger_params()
        if self.__log_enable:
            self.__initLogger()


def runmainapp():
    try:
        app = MainApp()
        app.init()
        app.exec()
    except Exception as ex:
        print(f"Fatal mainapp error: {ex}")
        sys.exit(1)


def main():
    try:
        appname = "grblflow"
        config_file_name = "settings.json"
        devmode = False

        launcher = Launcher(appname=appname, config_file_name=config_file_name, devmode=devmode)
        launcher.parse_args()
        launcher.start_logger()

        os.environ.setdefault("DEBUG", launcher.rootdir)
        os.environ.setdefault("APPNAME", launcher.appname)

        # launcher.logger.debug("debug")
        # launcher.logger.info("info")
        # launcher.logger.warning("warning")
        # launcher.logger.error("test")
        # launcher.logger.critical('critical message')

        runmainapp()

    except RuntimeError as ex:
        print(ex)
        sys.exit(2)
    except Exception as ex:
        print(f"Fatal error: {ex}")
        sys.exit(1)


if __name__ == '__main__':
    main()
