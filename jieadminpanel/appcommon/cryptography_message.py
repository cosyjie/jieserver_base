from cryptography.fernet import Fernet
import base64

from django.conf import settings


def generate_fernet_key():
    return Fernet.generate_key()


def encrypt_password(password):
    fernet = Fernet(settings.ENCRYPT_KEY)
    encrypted_password = fernet.encrypt(password.encode())
    return base64.b64encode(encrypted_password).decode()


def decrypt_password(encrypted_password_b64):
    encrypted_password = base64.b64decode(encrypted_password_b64)
    fernet = Fernet(settings.ENCRYPT_KEY)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password


def generate_password(length=16, has_uppercase=True, has_lowercase=True, has_digits=True, has_special_chars=True):
    import random
    import string
    """
    生成安全密码

    参数:
        length (int): 密码长度，默认为8
        has_uppercase (bool): 是否包含大写字母，默认为True
        has_lowercase (bool): 是否包含小写字母，默认为True
        has_digits (bool): 是否包含数字，默认为True
        has_special_chars (bool): 是否包含特殊字符，默认为True

    返回:
        str: 生成的密码
    """
    # 定义密码中可能包含的字符集
    characters = []
    if has_uppercase:
        characters.extend(string.ascii_uppercase)
    if has_lowercase:
        characters.extend(string.ascii_lowercase)
    if has_digits:
        characters.extend(string.digits)
    if has_special_chars:
        characters.extend(
            string.punctuation.replace(' ', '').replace('"', '').replace("'", '')
            .replace("·", "").replace("/", "").replace("\\", "")
            .replace("(", "").replace(")", "").replace("^", "")
            .replace(">", "").replace("<", "").replace(";", "")
            .replace("@",'').replace("`", "").replace("|", "")
            .replace("~", "").replace(":", "").replace("{", "")
            .replace("}", "").replace("[", "").replace("]", "")

        )  # 包含了大多数特殊字符，但你可能需要移除某些不想要的字符

    # 从字符集中随机选择字符来生成密码
    password = ''.join(random.choice(characters) for _ in range(length))

    return password