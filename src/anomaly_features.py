# src/anomaly_features.py

import re
from collections import defaultdict


def get_message_length(log_line):
    """
    Returns the length of the log message.
    Useful as a basic feature for anomaly detection.
    """
    return len(log_line)


def get_log_level(log_line):
    """
    Converts the log level (e.g., DEBUG, INFO, ERROR) into a numeric scale.
    Helps quantify the severity of the log for further analysis.

    Returns:
        1 = DEBUG
        2 = INFO
        3 = WARNING
        4 = ERROR
        5 = CRITICAL
        0 = Not found
    """
    levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    for level in levels:
        if level in log_line:
            return levels.index(level) + 1
    return 0


def extract_ip(log_line):
    """
    Extracts an IP address from the log line using a regular expression.

    Returns:
        IP address as a string if found, otherwise None.
    """
    match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', log_line)
    return match.group() if match else None


class IPCache:
    """
    Tracks how many times each IP appears.
    Helps detect suspicious repeated access.
    """

    def __init__(self):
        self.ip_counts = defaultdict(int)

    def update_and_get_count(self, ip):
        """
        Updates count for the given IP and returns the current count.
        """
        if ip:
            self.ip_counts[ip] += 1
            return self.ip_counts[ip]
        return 0
