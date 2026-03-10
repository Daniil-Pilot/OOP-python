import re


def is_valid_email(email: str) -> bool:
    """
    Проверяет корректность email-адреса.
    """
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


def get_domain(email: str) -> str:
    """
    Извлекает домен из email-адреса.
    """
    if '@' in email:
        return email.split('@')[1]
    return ''


def get_username(email: str) -> str:
    """
    Извлекает имя пользователя из email-адреса.
    """
    if '@' in email:
        return email.split('@')[0]
    return ''


def normalize_email(email: str) -> str:
    """
    Приводит email к нижнему регистру.
    """
    return email.strip().lower() if email else ''


def validate_emails(email_list: list) -> dict:
    """
    Проверяет список email-адресов.
    """
    result = {'valid': [], 'invalid': []}
    
    for email in email_list:
        if is_valid_email(email):
            result['valid'].append(email)
        else:
            result['invalid'].append(email)
    
    return result


if __name__ == "__main__":
    test_emails = [
        "user@example.com",
        "test.user@domain.org",
        "invalid",
        "@nodomain.com",
        "noat.com",
        "User@Example.COM",
        "7777@fa.ru"
    ]
    
    print("Проверка email-адресов:\n")
    
    for email in test_emails:
        status = "V" if is_valid_email(email) else "X"
        print(f"{status} {email}")
    
    print(f"Всего: {len(test_emails)}")
    results = validate_emails(test_emails)
    print(f"Валидных: {len(results['valid'])}")
    print(f"Невалидных: {len(results['invalid'])}")