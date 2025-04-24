import re
from typing import Tuple, Optional

def parse_log_line(line: str) -> Tuple[Optional[str], Optional[str], str]:
    """
    Parses a log line into timestamp, log level, and message.

    Example line:
    2025-04-22 12:45:01 ERROR Failed login from 192.168.1.10
    """
    match = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.+)", line)
    if match:
        return match.group(1), match.group(2), match.group(3)
    else:
        return None, None, line.strip()
