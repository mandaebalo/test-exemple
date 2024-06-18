import sqlite3
import bcrypt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog

# Создание подключения к базе данных
con = sqlite3.connect('userDataBase.db')
con = sqlite3.connect('clientDataBase.db')
cursor = con.cursor()
global login_entry  

def show_client_data(login):
    global client_table

    # Получаем ID пользователя по логину
    cursor.execute("SELECT id FROM users WHERE login=?", (login,))
    user_id = cursor.fetchone()[0]

    # Получаем данные о клиентах, связанных с ответственным пользователем
    cursor.execute("SELECT * FROM clients WHERE responsible_fio = (SELECT fio FROM users WHERE id = ?)", (user_id,))
    clients = cursor.fetchall()

    # Создание окна для отображения клиентов
    client_window = tk.Toplevel(root)
    client_window.title("Клиенты")

    # Создание таблицы
    client_table = ttk.Treeview(client_window, columns=("Номер счета", "Фамилия", "Имя", "Отчество", "Дата рождения", "ИНН", "ФИО ответственного", "Статус"), show="headings")

    # Настройка заголовков столбцов
    client_table.heading("Номер счета", text="Номер счета")
    client_table.heading("Фамилия", text="Фамилия")
    client_table.heading("Имя", text="Имя")
    client_table.heading("Отчество", text="Отчество")
    client_table.heading("Дата рождения", text="Дата рождения")
    client_table.heading("ИНН", text="ИНН")
    client_table.heading("ФИО ответственного", text="ФИО ответственного")
    client_table.heading("Статус", text="Статус")

    # Заполнение таблицы данными
    for client in clients:
        client_table.insert("", tk.END, values=client)

    # Добавление столбца с кнопками для изменения статуса
    client_table.column("#0", width=0, stretch=False)
    client_table.column("Статус", width=100, anchor="center")
    client_table.heading("#0", text="")
    client_table.heading("Статус", text="Статус")
    for i in range(len(clients)):
        client_table.insert("", tk.END, values=clients[i], tags=("status", i))

    # Создание контекстного меню для изменения статуса
    def change_status(event):
        selected_item = client_table.identify_row(event.y)
        if selected_item:
            # Получение значения статуса из таблицы
            current_status = client_table.item(selected_item)["values"][7]

            # Создание диалогового окна для выбора нового статуса
            new_status = simpledialog.askstring("Изменить статус", f"Текущий статус: {current_status}\nВыберите новый статус:",
                                                initialvalue=current_status,
                                                parent=client_window)
            if new_status:
                # Обновление статуса в базе данных
                client_id = client_table.item(selected_item)["values"][0]
                cursor.execute("UPDATE clients SET status=? WHERE account_number=?", (new_status, client_id))
                con.commit()

                # Обновление отображения статуса в таблице
                client_table.item(selected_item, values=(
                    client_table.item(selected_item)["values"][0],
                    client_table.item(selected_item)["values"][1],
                    client_table.item(selected_item)["values"][2],
                    client_table.item(selected_item)["values"][3],
                    client_table.item(selected_item)["values"][4],
                    client_table.item(selected_item)["values"][5],
                    client_table.item(selected_item)["values"][6],
                    new_status
                ))
    
    # Привязка контекстного меню к таблице
    client_table.bind("<Button-3>", change_status)

    client_table.pack()

# Создание главного окна
root = tk.Tk()
root.title("Авторизация")


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()

# Функция для проверки пароля
def check_password(provided_password, stored_hashed_password):
    return bcrypt.checkpw(provided_password.encode(), stored_hashed_password.encode())

# Функция для авторизации
def login_user():
    login = login_entry.get()
    password = password_entry.get()

    cursor.execute("SELECT password FROM users WHERE login=?", (login,))
    result = cursor.fetchone()

    if result:
        stored_hashed_password = result[0]
        if check_password(password, stored_hashed_password):
            # Авторизация успешна, открываем главный экран
            login_window.destroy()
            show_client_data(login)
        else:
            messagebox.showerror("Ошибка", "Неверный пароль")
    else:
        messagebox.showerror("Ошибка", "Неверный логин")

# Функция для регистрации нового пользователя
def register_user():
    last_name = last_name_entry.get()
    first_name = first_name_entry.get()
    middle_name = middle_name_entry.get()
    login = login_entry.get()
    password = password_entry.get()

    if not all([last_name, first_name, middle_name, login, password]):
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
        return

    # Проверка уникальности логина
    cursor.execute("SELECT COUNT(*) FROM users WHERE login=?", (login,))
    if cursor.fetchone()[0] > 0:
        messagebox.showerror("Ошибка", "Логин уже занят.")
        return

    # Хеширование пароля
    hashed_password = hash_password(password)

    try:
        # Вставка нового пользователя в базу данных
        cursor.execute(
            "INSERT INTO users (last_name, first_name, middle_name, login, password) VALUES (?, ?, ?, ?, ?)",
            (last_name, first_name, middle_name, login, hashed_password)
        )
        con.commit()
        messagebox.showinfo("Успех", "Регистрация прошла успешно.")
        register_window.destroy()
        login_window.deiconify()  # Показать окно авторизации
    except sqlite3.IntegrityError:
        messagebox.showerror("Ошибка", "Ошибка при регистрации.")

# Функция для отображения таблицы клиентов
def show_client_data(login):
    global client_table

    # Получаем ID пользователя по логину
    cursor.execute("SELECT id FROM users WHERE login=?", (login,))
    user_id = cursor.fetchone()[0]

    # Выбираем данные о клиентах, связанных с текущим пользователем
    cursor.execute("""
        SELECT 
            c.id,
            c.last_name,
            c.first_name,
            c.middle_name,
            c.status
        FROM clients c
JOIN responsible_persons rp ON c.responsible_person_id = rp.id
        JOIN users u ON rp.user_id = u.id
        WHERE u.id = ?
    """, (user_id,))

    clients = cursor.fetchall()

    # Создаем главное окно
    main_window = tk.Tk()
    main_window.title("Клиенты")

    # Создаем таблицу
    client_table = ttk.Treeview(main_window, columns=("id", "Фамилия", "Имя", "Отчество", "Статус"), show="headings")
    client_table.heading("id", text="ID")
    client_table.heading("Фамилия", text="Фамилия")
    client_table.heading("Имя", text="Имя")
    client_table.heading("Отчество", text="Отчество")
    client_table.heading("Статус", text="Статус")
    client_table.pack()

    # Заполняем таблицу данными
    for client in clients:
        client_table.insert("", "end", values=client)

    # Добавляем кнопку для изменения статуса клиента
    def update_client_status():
        selected_client = client_table.selection()
        if selected_client:
            client_id = client_table.item(selected_client[0])["values"][0]
            
            # Получаем текущий статус клиента
            cursor.execute("SELECT status FROM clients WHERE id = ?", (client_id,))
            current_status = cursor.fetchone()[0]

            # Открываем диалоговое окно для ввода нового статуса
            new_status = simpledialog.askstring("Изменить статус", f"Текущий статус: {current_status}\nВведите новый статус:", initialvalue=current_status)

            if new_status is not None:
                try:
                    # Обновляем статус клиента в базе данных
                    cursor.execute("UPDATE clients SET status = ? WHERE id = ?", (new_status, client_id))
                    con.commit()

                    # Обновляем таблицу
                    client_table.item(selected_client[0], values=(client_id, *client_table.item(selected_client[0])["values"][1:4], new_status))

                    messagebox.showinfo("Успех", "Статус клиента успешно изменен.")
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Ошибка при изменении статуса: {e}")

    # Кнопка "Изменить статус"
    update_status_button = tk.Button(main_window, text="Изменить статус", command=update_client_status)
    update_status_button.pack()

    main_window.mainloop()

# Окно авторизации
login_window = tk.Tk()
login_window.title("Авторизация")

login_label = tk.Label(login_window, text="Логин:")
login_label.grid(row=0, column=0)

login_entry = tk.Entry(login_window)
login_entry.grid(row=0, column=1)

password_label = tk.Label(login_window, text="Пароль:")
password_label.grid(row=1, column=0)
password_entry = tk.Entry(login_window, show="*")
password_entry.grid(row=1, column=1)

login_button = tk.Button(login_window, text="Войти", command=login_user)
login_button.grid(row=2, column=0, columnspan=2)

register_button = tk.Button(login_window, text="Регистрация", command=lambda: register_window.deiconify())
register_button.grid(row=3, column=0, columnspan=2)

# Окно регистрации
register_window = tk.Tk()
register_window.title("Регистрация")
register_window.withdraw()  # Скрыть окно регистрации по умолчанию

last_name_label = tk.Label(register_window, text="Фамилия:")
last_name_label.grid(row=0, column=0)
last_name_entry = tk.Entry(register_window)
last_name_entry.grid(row=0, column=1)

first_name_label = tk.Label(register_window, text="Имя:")
first_name_label.grid(row=1, column=0)
first_name_entry = tk.Entry(register_window)
first_name_entry.grid(row=1, column=1)

middle_name_label = tk.Label(register_window, text="Отчество:")
middle_name_label.grid(row=2, column=0)
middle_name_entry = tk.Entry(register_window)
middle_name_entry.grid(row=2, column=1)

login_label = tk.Label(register_window, text="Логин:")
login_label.grid(row=3, column=0)
login_entry = tk.Entry(register_window)
login_entry.grid(row=3, column=1)

password_label = tk.Label(register_window, text="Пароль:")
password_label.grid(row=4, column=0)
password_entry = tk.Entry(register_window, show="*")
password_entry.grid(row=4, column=1)

register_button = tk.Button(register_window, text="Зарегистрироваться", command=register_user)
register_button.grid(row=5, column=0, columnspan=2)

login_window.mainloop()
