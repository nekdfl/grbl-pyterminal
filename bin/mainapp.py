# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8

import json
import logging
import os
from logging.handlers import TimedRotatingFileHandler

import time
from datetime import datetime
import lib.utils as utils
# from pmodules.dispatcherutils.ftpclient import FtpClient
# from pmodules.ytankergrabber.ytgrabber import YTGrabber
# from pmodules.ytankergrabber.ytgrabberparams import YTGrabberParams



class MainApp:
    def __log(self):
        pass

    def __init__(self, rootdir):
        self.__rootdir = rootdir


    def __del__(self):
       self.logger.info("exit from application")

    def __check_mainapp_params(self, configdir, configname, logdir):
        def is_dir_exists(path):
            if not os.path.isdir(configdir):
                raise RuntimeError(
                    f"{path} is not directory or not exists")

        def is_file_exists(path):
            if not os.path.isfile(config):
                raise RuntimeError(
                    f"{path} is not file or not exists")

        config = os.path.join(configdir, configname)

        is_dir_exists(configdir)
        is_file_exists(config)
        is_dir_exists(logdir)


    def __loadconfig(self, configname):
        try:
            with open(configname, 'r') as f:
                config = json.load(f)

            self.__gconfig = config
        except Exception as ex:
            raise Exception(f"loadconfig error: {ex}")

    def __init_logger_params(self):
        self.__logbackupcnt = utils.getConfigValueDefVal(
            self.__gconfig, "/settings/logger/backupCount", 33)
        self.__enabledebug = bool(utils.getConfigValueDefVal(
            self.__gconfig, "/settings/logger/enableDebug", False))

    def __init_logger(self, logdir, filename, loggername):
        try:
            self.logger = logging.getLogger(loggername)
            fullpathlogdir = os.path.join(self.__rootdir, logdir)
            self.__logfilename = os.path.join(fullpathlogdir, filename)
            logbackupcnt = utils.getConfigValueDefVal(
                self.__gconfig, "/settings/logger/backupCount", 33)
            enabledebug = bool(utils.getConfigValueDefVal(
                self.__gconfig, "/settings/logger/enableDebug", False))
            fh = logging.handlers.TimedRotatingFileHandler(
                filename=self.__logfilename, backupCount=logbackupcnt, when='midnight')

            formatter = logging.Formatter(
                u'[%(asctime)s] [FILE:%(filename)s] [LINE:%(lineno)d]# %(levelname)s\t : %(message)s')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
            self.logger.setLevel(logging.INFO)

            if enabledebug is True:
                self.logger.setLevel(logging.DEBUG)

            self.logger.debug(f"logfile: {self.__logfilename}")
        except Exception as ex:
            raise Exception(f"init logger error: {ex}")

    def __init_application(self):
        pass

    def init(self):
        pass
        applicationname = "mainapp"
        ctime = datetime.now().strftime('%H%M_%d%m%Y')
        configdir = os.path.join(self.__rootdir, "etc")
        configname = os.path.join(configdir, "settings.json")
        logdir = os.path.join(self.__rootdir, "var", "log")
        logfilename = f"{applicationname}-{ctime}.log"

        self.__check_mainapp_params(configdir, configname, logdir)
        self.__loadconfig(configname)
        self.__init_logger(logdir, logfilename, applicationname)
        self.__init_application()
        self.logger.info("MainApp init successful")

    def __application_do_work(self):
        pass

    def do_dispatch(self):
        pass
        self.logger.debug("Do Dispatch")

        self.logger.info("Dispatch done")
