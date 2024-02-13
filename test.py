from plogging import Plogger

logger = Plogger(__name__, level=[0])

logger.debug("debugtest")
logger.info("infotest")
logger.warning("warningtest")
logger.critical("criticaltest")
logger.error("errorrtest")