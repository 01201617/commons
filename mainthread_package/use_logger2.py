""" 外からselfmade_loggerを活用する事例　

    root-- log_package -- basic -- selfmade_logger.py
    を想定して記述。

    これを機に、脱print文 !!
"""

from log_package.basic import selfmade_logger
from logging import DEBUG

# 開発時は、出力レベル(handler_level)をDEBUGにしておき、開発後は、INFOにしておく！
logger = selfmade_logger.get_module_logger(__name__, h_level=DEBUG)


def get_pengin(input):
    logger.debug({'input': input})
    return 'pengin'.format(input)