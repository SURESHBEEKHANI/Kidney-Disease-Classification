# Import necessary modules
import os  # For interacting with the operating system, e.g., file handling
from box.exceptions import BoxValueError  # Exception class for handling specific errors from 'Box'
import yaml  # For parsing and handling YAML files
from cnnClassifier import logger  # Custom logger for logging messages (assumed to be in cnnClassifier module)
import json  # For reading and writing JSON files
import joblib  # For saving and loading binary files (pickle-like)
from ensure import ensure_annotations  # Ensures function annotations for parameter validation
from box import ConfigBox  # Provides a dictionary-like object with attribute-style access
from pathlib import Path  # For easy handling of file system paths
from typing import Any  # For specifying dynamic data types in annotations
import base64  # For encoding and decoding binary data as base64 strings


# Define a function to read YAML files with strict type annotations
@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Reads a YAML file and returns its content.

    Args:
        path_to_yaml (Path): The file path to the YAML file

    Raises:
        ValueError: If the YAML file is empty
        e: Any other exceptions

    Returns:
        ConfigBox: The loaded YAML content as a ConfigBox object
    """
    try:
        with open(path_to_yaml) as yaml_file:  # Open the YAML file for reading
            content = yaml.safe_load(yaml_file)  # Safely load the YAML content
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")  # Log successful load
            return ConfigBox(content)  # Return content as ConfigBox
    except BoxValueError:  # Handle empty YAML file error
        raise ValueError("yaml file is empty")
    except Exception as e:  # Handle any other exceptions
        raise e


# Define a function to create directories with type annotations
@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """Creates a list of directories.

    Args:
        path_to_directories (list): List of directory paths to be created
        verbose (bool): If True, logs each directory creation
    """
    for path in path_to_directories:  # Iterate over directory paths
        os.makedirs(path, exist_ok=True)  # Create directory; do nothing if it exists
        if verbose:  # Log if verbose is True
            logger.info(f"created directory at: {path}")


# Define a function to save data to a JSON file
@ensure_annotations
def save_json(path: Path, data: dict):
    """Saves data to a JSON file.

    Args:
        path (Path): The file path to save the JSON data
        data (dict): Data to be saved in the JSON file
    """
    with open(path, "w") as f:  # Open file in write mode
        json.dump(data, f, indent=4)  # Dump data into JSON format with indentation

    logger.info(f"json file saved at: {path}")  # Log successful save


# Define a function to load data from a JSON file
@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """Loads data from a JSON file.

    Args:
        path (Path): The file path to the JSON file

    Returns:
        ConfigBox: The loaded data with attribute-style access
    """
    with open(path) as f:  # Open file in read mode
        content = json.load(f)  # Load JSON content

    logger.info(f"json file loaded successfully from: {path}")  # Log successful load
    return ConfigBox(content)  # Return data as ConfigBox


# Define a function to save data in binary format
@ensure_annotations
def save_bin(data: Any, path: Path):
    """Saves data as a binary file.

    Args:
        data (Any): Data to be saved in binary format
        path (Path): The file path to save the binary file
    """
    joblib.dump(value=data, filename=path)  # Save data as binary using joblib
    logger.info(f"binary file saved at: {path}")  # Log successful save


# Define a function to load data from a binary file
@ensure_annotations
def load_bin(path: Path) -> Any:
    """Loads binary data from a file.

    Args:
        path (Path): The file path to the binary file

    Returns:
        Any: The loaded binary data
    """
    data = joblib.load(path)  # Load binary data
    logger.info(f"binary file loaded from: {path}")  # Log successful load
    return data


# Define a function to get the size of a file in KB
@ensure_annotations
def get_size(path: Path) -> str:
    """Gets the file size in KB.

    Args:
        path (Path): The file path

    Returns:
        str: The file size in KB
    """
    size_in_kb = round(os.path.getsize(path) / 1024)  # Get size in KB by dividing by 1024
    return f"~ {size_in_kb} KB"  # Return formatted size string


# Define a function to decode a base64-encoded image string and save it to a file
def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)  # Decode base64 image string
    with open(fileName, 'wb') as f:  # Open file in binary write mode
        f.write(imgdata)  # Write decoded data to file
        f.close()  # Close the file


# Define a function to encode an image file into a base64 string
def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:  # Open image file in binary read mode
        return base64.b64encode(f.read())  # Encode file content to base64 and return
