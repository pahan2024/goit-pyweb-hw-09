import json
import os


def validate_json_files(quotes_path="quotes.json", authors_path="authors.json"):
    print("=" * 50)
    print("🏁 ЗАПУСК ВАЛІДАЦІЇ ДАНИХ ПЕРЕД ІМПОРТОМ")
    print("=" * 50)

    # 1. Перевірка наявності файлів
    if not os.path.exists(quotes_path) or not os.path.exists(authors_path):
        print("❌ ПОМИЛКА: Один або обидва файли JSON відсутні!")
        if not os.path.exists(quotes_path):
            print(f" - Не знайдено: {quotes_path}")
        if not os.path.exists(authors_path):
            print(f" - Не знайдено: {authors_path}")
        return False

    # 2. Завантаження даних
    try:
        with open(quotes_path, "r", encoding="utf-8") as f:
            quotes = json.load(f)
        with open(authors_path, "r", encoding="utf-8") as f:
            authors = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ ПОМИЛКА: Пошкоджений формат JSON файлів! {e}")
        return False

    print(f"📦 Знайдено цитат в {quotes_path}: {len(quotes)}")
    print(f"👤 Знайдено авторів в {authors_path}: {len(authors)}")
    print("-" * 50)

    # 3. Збір унікальних авторів з файлу цитат
    unique_authors_in_quotes = set()
    for item in quotes:
        if "author" in item:
            # Очищаємо від зайвих пробілів про всяк випадок
            unique_authors_in_quotes.add(item["author"].strip())
        else:
            print(f"⚠️ ПОПЕРЕДЖЕННЯ: Знайдено цитату без поля 'author': {item}")

    # 4. Збір імен авторів з файлу профілів авторів
    authors_profiles_names = set()
    for item in authors:
        if "fullname" in item:
            authors_profiles_names.add(item["fullname"].strip())
        else:
            print(
                f"⚠️ ПОПЕРЕДЖЕННЯ: Знайдено профіль автора без поля 'fullname': {item}"
            )

    # 5. Аналіз розбіжностей (пошук missing авторів)
    missing_authors = unique_authors_in_quotes - authors_profiles_names

    # 6. Виведення результатів
    if missing_authors:
        print(
            f"❌ КРИТИЧНА НЕВІДПОВІДНІСТЬ: Знайдено {len(missing_authors)} авторів, які є в цитатах, але відсутні в списку профілів!"
        )
        print("Невідповідні автори:")
        for author in sorted(missing_authors):
            print(f"  - {author}")
        print("\n🛑 Імпорт у базу даних ЗАБОРОНЕНО. Перезапустіть скрапер main.py.")
        return False
    else:
        print("✅ УСПІХ: Дані повністю синхронізовані!")
        print(
            f"Всі {len(unique_authors_in_quotes)} унікальних авторів мають свої профілі в {authors_path}."
        )
        print("🚀 Дані готові до безпечного імпорту в MongoDB!")
        return True


if __name__ == "__main__":
    validate_json_files()
