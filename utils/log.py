import logging
import datetime
import logging.handlers
import os

class Logger():
    def get_logger(self):
        alllog_file = os.path.abspath("log") + '/all.log'
        errlog_file = os.path.abspath("log") + '/error.log'
        logger = logging.getLogger("mylogger1")
        # 设置日志记录的最低级别
        logger.setLevel(logging.DEBUG)
        rf_handler = logging.handlers.TimedRotatingFileHandler(
            alllog_file,
            when = 'midnight',
            interval=1,
            backupCount=7,
            atTime = datetime.time(0, 0, 0, 0)
        )
        rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        f_handler = logging.FileHandler(errlog_file)
        f_handler.setLevel(logging.ERROR)
        f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
        logger.addHandler(rf_handler)
        logger.addHandler(f_handler)
        return logger

if __name__ == "__main__":
    logger = Logger().get_logger()
    logger.error('error.log')
    logger.warning("warn log")
    logger.info("info log")
    logger.debug("debug log")
    logger.critical("critical log")