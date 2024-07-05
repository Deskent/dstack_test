from pathlib import Path

from .logger_config import make_logger

BASE_DIR: Path = Path().cwd()
LOGS_DIR: Path = BASE_DIR / 'logs'

logger = make_logger(
    logger_name='docker_parser',
    level=1,
    base_logger_dir=LOGS_DIR,
)
