""" 外からselfmade_loggerを活用する事例　

    root-- log_package -- basic -- selfmade_logger.py
    を想定して記述。

    これを機に、脱print文 !!

"""

from log_package.basic import selfmade_logger
from logging import DEBUG

from mainthread_package import use_logger2

if __name__=='__main__':
    # 開発時は、出力レベル(handler_level)をDEBUGにしておき、開発後は、INFOにしておく！
    logger = selfmade_logger.get_module_logger(__name__, h_level=DEBUG)

    logger.info('from_outside')
    logger.debug('from_outside')

    # 変数をdictで表記

    param1 = 'ペンギンハイウェイ'
    param2 = 1989

    # 複数は、辞書型で、ロギング
    logger.debug({
        'param1' : param1,
        'param2' : param2
    })

    # 短ければ、1行で、ロギングOK!
    logger.critical({'param1' : param1, 'param2' : param2})

    logger.debug(use_logger2.get_pengin('確認'))