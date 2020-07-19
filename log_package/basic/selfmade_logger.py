
from logging import getLogger, StreamHandler, DEBUG, Formatter, FileHandler, CRITICAL, INFO
import os
import datetime

def  get_module_logger(modname, h_level=INFO):
    """複数のファイルにまたがるモジュールで共通のloggerを使用する場合"""
    # インスタンス化
    logger = getLogger(modname)

    # ハンドラーの設定(console and file)
    handler = StreamHandler()
    h_format = Formatter("%(asctime)0.19s - %(module)s [%(levelname)s] %(message)s ")
    handler.setFormatter(h_format)
    handler.setLevel(DEBUG)
    logger.setLevel(DEBUG)
    logger.addHandler(handler)

    current_dicectory = os.path.dirname(__file__)
    try:
        os.mkdir(current_dicectory + '/logfile')
    except FileExistsError:
        pass
    get_handler = FileHandler(current_dicectory+'/logfile/logger.log')
    get_handler.setLevel(h_level)
    get_handler.setFormatter(h_format)
    logger.addHandler(get_handler)
    logger.propagate = False

    return logger


if __name__ =='__main__':
    logger = get_module_logger(__name__, h_level=INFO)
    logger.debug('hello')
    logger.info('info')
    logger.critical('critical')





