from utils.maap_logger import MaapLogger
from functools import lru_cache
import sys
import config

@lru_cache()
def get_logger():
    """Get a singleton logger instance."""
    try:
        return MaapLogger(service_url=config.LOGGER_SERVICE_URL, app_name=config.APP_NAME)
    except Exception:
        # Fallback to basic logging if MAAP logger is not available
        import logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            stream=sys.stdout
        )
        return logging.getLogger(config.APP_NAME)

# Export logger for convenience
logger = get_logger()