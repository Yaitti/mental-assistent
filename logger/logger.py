import logging
import sys


APP_LOGGER_NAME = "MentalAssistant"

def set_app_lvl_logger(logger_name=APP_LOGGER_NAME):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(f'{__name__}.log', mode="w")
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def get_logger(module_name):
    return logging.getLogger(APP_LOGGER_NAME).getChild(module_name)