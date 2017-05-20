import keyring
from cryptography.fernet import Fernet


def set_creds(service, username, password):
    if isinstance(password, str):
        password = password.encode('utf-8')

    key = Fernet.generate_key()

    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(password).decode('utf-8')

    keyring.set_password(service, username, cipher_text)

    return key


def get_creds(service, username, key):
    if isinstance(key, str):
        key = key.encode('utf-8')

    cipher_text = keyring.get_password(service, username).encode('utf-8')
    cipher_suite = Fernet(key)

    password = cipher_suite.decrypt(cipher_text).decode('utf-8')

    return password


if __name__ == '__main__':
    pass
