from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

def encrypt_password (password: str) -> str:
    return f.encrypt(password.encode('utf-8')).decode('utf-8')