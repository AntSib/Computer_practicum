def caesar_encrypt(secret: str, key: int) -> str:
    """
    Encrypts a given string with a Caesar cipher.

    :param secret: The string to encrypt
    :param key: The key to use for the encryption
    :return: The encrypted string
    """
    result = []
    for char in secret:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            # Смещение с учетом алфавита
            shifted = (ord(char) - base + key) % 26
            result.append(chr(base + shifted))
        else:
            result.append(char)  # Не шифруем прочие символы
    return ''.join(result)

def caesar_decrypt(secret: str, key: int) -> str:
    """
    Decrypts a given string with a Caesar cipher.

    :param secret: The string to decrypt
    :param key: The key to use for the decryption
    :return: The decrypted string
    """
    return caesar_encrypt(secret, -key)
