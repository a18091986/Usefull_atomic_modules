import logging

from utils.text import print_info

logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode='w',
                    format="%(name)s %(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger()

logging.getLogger('aiogram').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('asyncio').setLevel(logging.WARNING)


def log_in_file_and_print_in_terminal(msg: str, print_in_terminal=False, loglevel=0):
    if loglevel == 0:
        logger.debug(msg=msg)
    elif loglevel == 1:
        logger.warning(msg=msg)
    elif loglevel == 2:
        logger.error(msg=msg)
    elif loglevel == 3:
        logger.critical(msg=msg)
    else:
        logger.info(msg=msg)

    if print_in_terminal:
        print_info(msg=f'{" " * 5}|{msg}|{" " * 5}', color="синий", print_separator_after=True, separator='-')
