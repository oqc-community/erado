import logging


def configure_logging() -> None:
    FORMAT = "%(levelname)s:%(filename)11s:%(lineno)2d - %(message)s"
    logging.basicConfig(level=logging.INFO, format=FORMAT)
