import random
import string


def generate_password(length=12, use_special=True):
    """Генерация случайного пароля"""
    chars = string.ascii_letters + string.digits
    if use_special:
        chars += "!@#$%^&*"
    
    return ''.join(random.choice(chars) for i in range(length))


def check_password(password):
    """Проверка надежности пароля"""
    if len(password) < 8:
        return "Слабый"
    elif len(password) < 12:
        return "Средний"
    else:
        return "Надежный"


if __name__ == "__main__":
    pwd = generate_password(16)
    print(f"Пароль: {pwd}")
    print(f"Надежность: {check_password(pwd)}")