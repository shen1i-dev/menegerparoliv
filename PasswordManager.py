import json
import os
from datetime import datetime
from tabulate import tabulate

FILE_NAME = "passwords.json"


class PasswordManager:

    def __init__(self):
        self.data = self.load_data()

    # ---------------- FILE ----------------
    def load_data(self):
        if not os.path.exists(FILE_NAME):
            return []

        try:
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_data(self):
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    # ---------------- CORE ----------------
    def add_record(self):
        service = input("Сервіс: ").strip()
        login = input("Логін: ").strip()
        password = input("Пароль: ").strip()

        if not service or not login or not password:
            print("Усі поля обов'язкові")
            return

        # перевірка на дублікати
        for r in self.data:
            if r["service"].lower() == service.lower():
                print(" Такий сервіс вже існує")
                return

        record = {
            "service": service,
            "login": login,
            "password": password,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        self.data.append(record)
        self.save_data()
        print("Запис додано")

    def show_records(self):
        if not self.data:
            print("Список порожній")
            return

        table = []

        for i, r in enumerate(self.data, start=1):
            table.append([
                i,
                r["service"],
                r["login"],
                "*" * len(r["password"]),
                r["created_at"],
                r["updated_at"]
            ])

        print(tabulate(
            table,
            headers=["№", "Сервіс", "Логін", "Пароль", "Створено", "Оновлено"],
            tablefmt="grid"
        ))

    def search_record(self):
        query = input("Введіть сервіс: ").strip().lower()

        found = False

        for r in self.data:
            if query in r["service"].lower():
                print("\n🔎 ЗНАЙДЕНО:")
                print(f"Сервіс: {r['service']}")
                print(f"Логін: {r['login']}")
                print(f"Пароль: {'*' * len(r['password'])}")
                print(f"Створено: {r['created_at']}")
                print(f"Оновлено: {r['updated_at']}")
                found = True

        if not found:
            print(" Нічого не знайдено")

    def edit_record(self):
        service = input("Сервіс для редагування: ").strip().lower()

        for r in self.data:
            if r["service"].lower() == service:

                print("Залиш порожнім, якщо не змінюєш")

                new_service = input(f"Сервіс ({r['service']}): ").strip()
                new_login = input(f"Логін ({r['login']}): ").strip()
                new_password = input("Пароль: ").strip()

                if new_service:
                    r["service"] = new_service
                if new_login:
                    r["login"] = new_login
                if new_password:
                    r["password"] = new_password

                r["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

                self.save_data()
                print("Оновлено")
                return

        print("Не знайдено")

    def delete_record(self):
        service = input("Сервіс для видалення: ").strip().lower()

        for r in self.data:
            if r["service"].lower() == service:
                self.data.remove(r)
                self.save_data()
                print("🗑 Видалено")
                return

        print(" Не знайдено")

    def sort_records(self):
        self.data.sort(key=lambda x: x["service"].lower())
        self.save_data()
        print("↕ Відсортовано")

    # ---------------- MENU ----------------
    def menu(self):
        while True:
            print("\n===== PASSWORD MANAGER =====")
            print("1. Додати запис")
            print("2. Показати всі")
            print("3. Пошук")
            print("4. Редагувати")
            print("5. Видалити")
            print("6. Сортувати")
            print("0. Вихід")

            choice = input(">>> ").strip()

            if choice == "1":
                self.add_record()
            elif choice == "2":
                self.show_records()
            elif choice == "3":
                self.search_record()
            elif choice == "4":
                self.edit_record()
            elif choice == "5":
                self.delete_record()
            elif choice == "6":
                self.sort_records()
            elif choice == "0":
                print("Вихід...")
                break
            else:
                print("Невірний вибір")

#python PasswordManager.py запуск програми

if __name__ == "__main__":
    app = PasswordManager()
    app.menu()