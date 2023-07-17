import json
from utils.crypto_utils import encrypt_aes, generate_key
from utils.logger_utils import logger

def read_content(path : str) -> dict:
    """
    Reads content from a JSON file.

    Args:
        path (str): The path to the JSON file.

    Returns:
        dict: A dictionary containing the jsons content.
    """
    with open(path, "r") as input_file:
        data : dict = json.load(input_file)
    return data

def encrypt_credentials(path : str) -> dict|None:
    """
    Encrypts credentials using AES encryption.

    Args:
        path (str): The path to the JSON file containing the credentials.

    Returns:
        dict or None: A dictionary containing the encrypted credentials,
                      or None if an error occurs.
    """
    try:
        dict_credentials : dict = read_content(path)
        if not isinstance(dict_credentials, dict):
            logger.error("Invalid credentials format. Expected a dictionary.")
            return None
        dict_credentials["key"] = generate_key(32)
        dict_credentials["username"] = encrypt_aes(dict_credentials["username"], dict_credentials["key"])
        dict_credentials["password"] = encrypt_aes(dict_credentials["password"], dict_credentials["key"])    
        return dict_credentials
    except Exception as e:
        logger.error(f"Error when trying to encrypt the credentials: {e}")
    return None

def encrypted_credentials(path : str) -> bool:
    """
    Checks if credentials are encrypted or not. 

    Args:
        path (str): The path to the file containing the credentials.

    Returns:
        bool: True if encrypted credentials exist, False otherwise.
    """
    try:
        dict_credentials : dict = read_content(path)
    except Exception as e:
        logger.error(f"Error when trying to read the credentials: {e}")
    if dict_credentials["key"] == "":
        return False
    return True

def write_encrypted_credentials(path : str, updated_credentials : dict) -> None:
    """
    Writes the new encrypted credentials to the file. 

    Args:
        path (str): The path to the output file.
        updated_credentials (dict): The updated credentials to write.

    Returns:
        None
    """
    try:
        updated_json_credentials = json.dumps(updated_credentials)
        with open(path, "w") as output_file:
            output_file.write(updated_json_credentials)
    except Exception as e:
        logger.error(f"Error when writing in a the encrypted file: {e}")