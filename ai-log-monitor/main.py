import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))
from src.monitor import start_monitoring

if __name__ == "__main__":
    start_monitoring()
