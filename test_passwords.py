import json
import os
from PasswordManager import PasswordManager

TEST_FILE = "test_passwords.json"

def setup_manager():
    """Налаштовує менеджер для роботи з тимчасовим тестовим файлом."""
    # Тимчасово змінюємо ім'я файлу в модулі, щоб не затерти справжні паролі
    import PasswordManager as pm
    pm.FILE_NAME = TEST_FILE
    
    # Створюємо чистий екземпляр
    manager = PasswordManager()
    manager.data = []
    manager.save_data()
    return manager

def teardown():
    """Видаляє тимчасовий файл після тестів."""
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

# =====================================================================
# Тест 1: Додавання запису
# =====================================================================
manager = setup_manager()

# Імітуємо введення користувача для методів input() за допомогою lambda
inputs = ["Google", "user@gmail.com", "password123"]
builtins_input = __builtins__.input
__builtins__.input = lambda prompt="": inputs.pop(0)

try:
    manager.add_record()
finally:
    # Повертаємо стандартний input назад
    __builtins__.input = builtins_input

# Перевірка результату
assert len(manager.data) == 1, "Запис не було додано"
assert manager.data[0]["service"] == "Google"
assert manager.data[0]["login"] == "user@gmail.com"
assert manager.data[0]["password"] == "password123"
print(" Тест 1: Додавання запису виконано успішно.")


# =====================================================================
# Тест 2: Сортування записів
# =====================================================================
# Додамо вручну ще кілька записів для тесту сортування
manager.data.append({
    "service": "Apple", "login": "apple_id", "password": "abc", 
    "created_at": "2026-06-21 12:00", "updated_at": "2026-06-21 12:00"
})
manager.save_data()

# Сортуємо (має бути Apple, а потім Google)
manager.sort_records()

assert manager.data[0]["service"] == "Apple", "Сортування відпрацювало некоректно"
assert manager.data[1]["service"] == "Google", "Сортування відпрацювало некоректно"
print(" Тест 2: Сортування записів за алфавітом працює.")


# =====================================================================
# Тест 3: Видалення запису
# =====================================================================
# Імітуємо введення сервісу для видалення
inputs = ["apple"]
__builtins__.input = lambda prompt="": inputs.pop(0)

try:
    manager.delete_record()
finally:
    __builtins__.input = builtins_input

# Після видалення "Apple" має залишитися тільки 1 запис ("Google")
assert len(manager.data) == 1, "Запис не було видалено"
assert manager.data[0]["service"] == "Google", "Видалився не той запис"
print(" Тест 3: Видалення запису працює коректно.")

# Очищення після тестів
teardown()
print("\nУсі тести для PasswordManager пройдено успішно! 🎉")