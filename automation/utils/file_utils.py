import json
from utils.crypto_utils import encrypt_aes, generate_key

def read_credentials(path : str) -> dict:
    """
    Reads credentials from a JSON file.

    Args:
        path (str): The path to the JSON file.

    Returns:
        dict: A dictionary containing the credentials.
    """
    with open(path, "r") as input_file:
        data : dict = json.load(input_file)
    return data

def encrypt_credentials(path : str) -> dict:
    dict_credentials : dict = read_credentials(path)
    dict_credentials["key"] = generate_key(32)
    dict_credentials["username"] = encrypt_aes(dict_credentials["username"], dict_credentials["key"])
    dict_credentials["password"] = encrypt_aes(dict_credentials["password"], dict_credentials["key"])    
    return dict_credentials

def encrypted_credentials(path : str) -> bool:
    dict_credentials : dict = read_credentials(path)
    if dict_credentials["key"] == "":
        return False
    return True

def write_new_encrypted_credentials(path : str, updated_credentials : dict) -> None:
    updated_json_credentials = json.dumps(updated_credentials)
    with open(path, "w") as output_file:
        output_file.write(updated_json_credentials)