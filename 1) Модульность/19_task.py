from password_generator import generate_password, check_password

password = generate_password(16)

strength = check_password(password)

print(f"Пароль: {password}")
print(f"Надежность: {strength}")