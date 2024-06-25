import logging
import logging.config


logger = logging.getLogger("app")


def i(msg):
    logger.info(msg)


def d(msg):
    logger.debug(msg)


def w(msg):
    logger.warning(msg)


def e(msg):
    logger.error(msg)


def ex(e):
    logger.exception(e)
