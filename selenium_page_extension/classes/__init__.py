import configparser
import logging

conf = configparser.ConfigParser()

conf.read("selenium_extension.ini")

wait_presence = conf.getint("selenium_ext", "wait_for_presence", fallback=20)
wait_interaction = conf.getint("selenium_ext", "wait_for_interaction", fallback=20)

logger = logging.getLogger(__name__)

logger.info("\n".join([
    "selenium extension started with parameters:",
    f"\t{wait_presence=}",
    f"\t{wait_interaction=}"
]
))
