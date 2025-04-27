# src/cloud_logger.py

import logging
import watchtower


def get_cloudwatch_logger(log_group="ai-log-monitor-group"):
    """
    Creates a logger that sends logs to AWS CloudWatch.

    Args:
        log_group (str): Name of the CloudWatch log group.

    Returns:
        Logger object configured for CloudWatch.
    """
    logger = logging.getLogger("cloudwatch")
    logger.setLevel(logging.INFO)

    handler = watchtower.CloudWatchLogHandler(log_group=log_group)
    logger.addHandler(handler)

    return logger
