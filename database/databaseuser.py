import sqlite3 as sl
import csv
import bcrypt


con = sl.connect('userDataBase.db')

with con:
    cursor = con.cursor()  # Создаем курсор для выполнения запросов

    cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='users'")
    result = cursor.fetchone()  # Получаем результат запроса

    if result[0] == 0:
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID пользователя (автоматически увеличивается)
                last_name TEXT,  -- Фамилия
                first_name TEXT,  -- Имя
                middle_name TEXT,  -- Отчество
                login TEXT UNIQUE,  -- Логин (уникальный)
                password TEXT  -- Пароль
                )
        ''')
        print("Таблица 'users' создана успешно.")
    else:
        print("Таблица 'users' уже существует.")
        

def hash_password(password):
    salt = bcrypt.gensalt()  # Генерируем соль
    hashed_password = bcrypt.hashpw(password.encode(), salt)  # Хешируем пароль с солью
    return hashed_password.decode()

def check_password(provided_password, stored_hashed_password):
    return bcrypt.checkpw(provided_password.encode(), stored_hashed_password.encode())

def add_user(last_name, first_name, middle_name, login, password):
    """Добавляет нового пользователя в базу данных.

    Args:
        last_name (str): Фамилия пользователя.
        first_name (str): Имя пользователя.
        middle_name (str): Отчество пользователя.
        login (str): Логин пользователя.
        password (str): Пароль пользователя.
    """
    hashed_password = hash_password(password)  # Хешируем пароль
    try:
        with con:
            cursor = con.cursor()
            cursor.execute(
                "INSERT INTO users (last_name, first_name, middle_name, login, password) VALUES (?, ?, ?, ?, ?)",
                (last_name, first_name, middle_name, login, hashed_password)
            )
            print("Пользователь добавлен в базу данных.")
    except sqlite3.IntegrityError:
        print("Ошибка: Логин уже существует.")


# Пример использования:

    
    
con.close()  # Закрываем соединение с базой данных
