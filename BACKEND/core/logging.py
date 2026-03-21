import logging
import os
from datetime import datetime


class HourlyFolderHandler(logging.Handler):
    def __init__(self, base_dir="logs"):
        super().__init__()
        self.base_dir = base_dir
        self.current_hour = None
        self.stream = None

    def get_log_file(self):
        now = datetime.now()

        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        hour = now.strftime("%H")

        folder = os.path.join(self.base_dir, year, month, day)
        os.makedirs(folder, exist_ok=True)

        filepath = os.path.join(folder, f"{hour}.log")

        return filepath, hour

    def emit(self, record):
        try:
            filepath, hour = self.get_log_file()

            # rotate file if hour changed
            if self.current_hour != hour:
                if self.stream:
                    self.stream.close()

                self.stream = open(filepath, "a", encoding="utf-8")
                self.current_hour = hour

            msg = self.format(record)
            self.stream.write(msg + "\n")
            self.stream.flush()

        except Exception:
            self.handleError(record)


# Logger setup
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

handler = HourlyFolderHandler("logs")

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

handler.setFormatter(formatter)

logger.addHandler(handler)