import logging
import watchtower

def get_cloudwatch_logger(log_group="ai-log-monitor-group"):
    logger = logging.getLogger("cloudwatch")
    logger.setLevel(logging.INFO)

    # Watchtower handler'ı ekle
    handler = watchtower.CloudWatchLogHandler(log_group=log_group)
    logger.addHandler(handler)

    return logger
