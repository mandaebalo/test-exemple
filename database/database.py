import sqlite3 as sl
import csv

con = sl.connect('clientDataBase.db')

with con:
    cursor = con.cursor()  # Создаем курсор для выполнения запросов

    cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='goods'")
    result = cursor.fetchone()  # Получаем результат запроса

    if result[0] == 0:
        cursor.execute('''
            CREATE TABLE goods (
                account_number INTEGER PRIMARY KEY,  -- Номер счета
                last_name TEXT,  -- Фамилия
                first_name TEXT,  -- Имя
                middle_name TEXT,  -- Отчество
                date_of_birth DATE,  -- Дата рождения
                INN TEXT,  -- ИНН
                responsible_name TEXT,  -- ФИО ответственного
                status TEXT  -- Статус
            )
        ''')
        print("Таблица 'goods' создана успешно.")
    else:
        print("Таблица 'goods' уже существует.")

'''  # Импорт данных из CSV-файла
   with open('../clients.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
        for row in reader:
            try:
                # Замените placeholders на реальные значения из row
                cursor.execute("INSERT INTO goods VALUES (?, ?, ?, ?, ?, ?, ?, ?)", row)
            except sqlite3.IntegrityError:
                print(f"Дубликат account_number: {row[0]}")
                continue  # Пропускаем строку с дубликатом'''

with con:
    data = con.execute("SELECT * FROM goods")
    for row in data:
        print(row)
        
con.close()  # Закрываем соединение с базой данных
