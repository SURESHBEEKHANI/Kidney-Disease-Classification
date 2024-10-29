# Import the 'os' module for interacting with the operating system, including file and directory management
import os

# Import the 'sys' module for accessing system-specific parameters and functions
import sys

# Import the 'logging' module for logging events for diagnostic purposes
import logging

# Define the log message format string with placeholders for timestamp, log level, module name, and message
logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

# Set the directory where log files will be stored
log_dir = "logs"

# Define the path to the log file by joining the directory path with the log file name
log_filepath = os.path.join(log_dir, "running_logs.log")

# Create the directory if it doesn't exist already, to avoid errors when creating log files
os.makedirs(log_dir, exist_ok=True)

# Configure the logging settings, specifying the log level, format, and output handlers
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO to capture informational messages and above
    format=logging_str,  # Use the defined logging format for each log message

    # Define two handlers: one to write logs to the file and another to output them to the console
    handlers=[
        logging.FileHandler(log_filepath),  # File handler to log messages to the specified log file
        logging.StreamHandler(sys.stdout)   # Stream handler to output logs to the console (stdout)
    ]
)

# Create a logger instance with the name 'cnnClassifierLogger' for logging specific to this application/module
logger = logging.getLogger("cnnClassifierLogger")
