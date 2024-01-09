from logger_config import configure_logger
from security.secure_encryptor import SecureCrypto
import os

root_directory = os.getcwd()
main_logger = configure_logger()
crypto_secret_key = b'O6vJtGEZmrq5cOhcfftPfwOCcAvfcG5hnIdgHO_NvUk='
secure_crypto = SecureCrypto(crypto_secret_key)
