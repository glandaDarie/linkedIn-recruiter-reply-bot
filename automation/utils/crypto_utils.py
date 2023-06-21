from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode

def generate_key(length: int = 16) -> str:
    """
    Generates a random key of the specified length.

    Args:
        length (int): The length of the key in bytes. Default is 16 bytes.

    Returns:
        str: The randomly generated key as a hex string.
    """
    return get_random_bytes(length).hex()
    
def encrypt_aes(message : str, key : str) -> str:
    """
    Encrypts the message string using AES encryption in CBC mode with PKCS7 padding.

    Args:
        key (str): The encryption key as a string.
        message (str): The message string to be encrypted.

    Returns:
        str: The encrypted message as a Base64-encoded string.
    """
    message : bytes = bytes(message, encoding="utf-8")
    key : bytes = bytes.fromhex(key)
    cipher : AES = AES.new(key, AES.MODE_CBC)
    ciphertext : bytes = cipher.encrypt(pad(message, AES.block_size))
    iv_and_ciphertext : bytes = cipher.iv + ciphertext
    encrypted_data : bytes = b64encode(iv_and_ciphertext).decode("utf-8")
    return encrypted_data

def decrypt_aes(encrypted_message : str, key : str) -> bytes:
    """
    Decrypts the encrypted message using AES decryption in CBC mode.

    Args:
        key (str): The decryption key as a string.
        encrypted_message (str): The Base64-encoded encrypted message to be decrypted.

    Returns:
        bytes: The decrypted data as a byte string.
    """
    key : bytes = bytes.fromhex(key)
    iv_and_ciphertext : bytes = b64decode(encrypted_message)
    iv : bytes = iv_and_ciphertext[:16]
    ciphertext : bytes = iv_and_ciphertext[16:]
    cipher : AES = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data : bytes = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_data

