from cryptography.fernet import Fernet


class SecureCrypto:
    def __init__(self, key: bytes):
        self.key = key
        self.cipher_suite = Fernet(key)

    def encrypt(self, data: str) -> bytes:
        """
        Encrypts the provided data using the initialized key.

        Args:
            data (str): The data to be encrypted.

        Returns:
            bytes: The encrypted data.
        """
        try:
            encrypted_data = self.cipher_suite.encrypt(data.encode())
            return encrypted_data
        except Exception as e:
            raise ValueError(f"Encryption error: {e}")

    def decrypt(self, encrypted_data: bytes) -> str:
        """
        Decrypts the provided encrypted data using the initialized key.

        Args:
            encrypted_data (bytes): The encrypted data to be decrypted.

        Returns:
            str: The decrypted data.
        """
        try:
            decrypted_data = self.cipher_suite.decrypt(encrypted_data).decode()
            return decrypted_data
        except Exception as e:
            raise ValueError(f"Decryption error: {e}")


