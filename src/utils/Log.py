import logging
from config.Constant import LOG_LEVEL


'''
有关日志的操作
'''


class Logging(object):
    def __init__(self, log_path=None):
        """
        日志类初始化
        :param log_path: 如果有路径则保存日志到文件，没有则只输出日志到控制台
        """
        self.log = logging.getLogger('main')
        level = {'DEBUG': logging.DEBUG,
                 'INFO': logging.INFO,
                 'WARNING': logging.WARNING,
                 'ERROR': logging.ERROR}[LOG_LEVEL]
        self.log.setLevel(level=level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        if log_path is not None:
            # 创建一个FileHandler，用于写到本地
            file_handler = logging.FileHandler(log_path, encoding='utf-8')
            file_handler.setLevel(level=logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.log.addHandler(file_handler)
            self.log.removeHandler(file_handler)
            file_handler.close()
        # 创建一个StreamHandler,用于输出到控制台
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level=logging.DEBUG)
        stream_handler.setFormatter(formatter)
        self.log.addHandler(stream_handler)
        self.log.removeHandler(stream_handler)

    def error(self, msg):
        self.log.error(msg)

    def warning(self, msg):
        self.log.warning(msg)

    def info(self, msg):
        self.log.info(msg)

    def debug(self, msg):
        self.log.debug(msg)
