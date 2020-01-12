import logging
from typing import Optional


class LoggerObject:
    def __init__(self, name: str, level: int) -> None:

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.date_format = '%m-%d-%Y'

    def add_handler(self,
        level: int,
        formatting: str,
        handler: logging.Handler,
        name: Optional[str]) -> None:

        if handler is logging.FileHandler:
            tmp = handler(name)
        else:
            tmp = handler()
        tmp.setLevel(level)
        tmp_format = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s:\n%(message)s",
            datefmt=self.date_format
        )
        tmp.setFormatter(tmp_format)

        self.logger.addHandler(tmp)

if __name__ == "__main__":

    test_format = "%(asctime)s: %(name)s - %(levelname)s\n %(message)s"

    logs = LoggerObject(name="logging_object", level=logging.DEBUG)
    logs.add_handler(
        name="test_handler",
        level=logging.WARNING,
        formatting=test_format,
        handler=logging.StreamHandler
    )
    print(logs)

    # logs.logger.info("hello!")
    # logs.logger.warning("hello with a warning!")