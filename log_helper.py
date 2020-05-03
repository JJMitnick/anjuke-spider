# -*-coding:utf-8-*-
# @time: 2020/5/3 11:12
# @author: Mitnick
# @description: 日志工具类

import logging
import logging.handlers


class LogHelper(object):
    def __init__(self, log_file=None, log_name=None):
        """
        初始化
        :param log_file: 例如:a.log
        :param log_name: 例如:log
        :return:
        """
        if log_file is None:
            raise ValueError('log file is none')
        if log_name is None:
            raise ValueError('log name is none')

        self.LOG_FILE = log_file
        self.LOG_NAME = log_name

    def get_logger(self):
        """
        ...
        :return:
        """
        handler = logging.handlers.RotatingFileHandler(self.LOG_FILE, maxBytes=1024 * 1024 * 10, backupCount=10)
        fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
        # 实例化formatter
        formatter = logging.Formatter(fmt)
        # 为handler添加formatter
        handler.setFormatter(formatter)
        # 获取名为tst的logger
        logger = logging.getLogger(self.LOG_NAME)
        # 为logger添加handler
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        return logger
