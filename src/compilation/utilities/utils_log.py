import logging
import logging.config

from utilities.utils import get_timestamp
from utilities.utils_config import load_config
from utilities.utils_path import project_root


def setup_logging():
    try:
        logging_config = load_config()["logging"]

        log_file_dir = project_root / logging_config["log_file_dir_name"]
        log_file_dir.mkdir(parents=True, exist_ok=True)

        timestamp = get_timestamp()
        log_file_name = logging_config["log_name_template"].format(timestamp=timestamp)
        log_file_path = log_file_dir / log_file_name

        for handler in logging_config["handlers"].values():
            if handler["class"] == "logging.FileHandler":
                handler["filename"] = log_file_path

        logging.config.dictConfig(logging_config)

    except Exception as e:
        logging.error(f"Error loading configuration file: {e}")
        logging.basicConfig(level=logging.INFO)


setup_logging()
logger = logging.getLogger("tri_cal")
logger.info("logger initialized")
