import random
import datetime

def generate_random_name(gender):
  """Генерирует случайное имя и отчество."""
  if gender == "мужской":
    first_names = ["Иван", "Алексей", "Дмитрий", "Сергей", "Андрей", "Александр", "Владимир", "Николай", "Михаил", "Максим"]
    last_names = ["Иванов", "Петров", "Сидоров", "Смирнов", "Кузнецов", "Васильев", "Соколов", "Попов", "Михайлов", "Федоров"]
    patronymic_names = ["Иванович", "Алексеевич", "Дмитриевич", "Сергеевич", "Андреевич", "Александрович", "Владимирович", "Николаевич", "Михайлович", "Максимович"]
  elif gender == "женский":
    first_names = ["Екатерина", "Мария", "Ирина", "Ольга", "Елена", "Наталья", "Татьяна", "Светлана", "Анна", "Юлия"]
    last_names = ["Иванова", "Петрова", "Сидорова", "Смирнова", "Кузнецова", "Васильева", "Соколова", "Попова", "Михайлова", "Федорова"]
    patronymic_names = ["Ивановна", "Алексеевна", "Дмитриевна", "Сергеевна", "Андреевна", "Александровна", "Владимировна", "Николаевна", "Михайловна", "Максимовна"]
  else:
    return None, None, None

  return random.choice(first_names), random.choice(last_names), random.choice(patronymic_names)

def generate_random_inn():
  """Генерирует случайный ИНН."""
  return str(random.randint(1000000000, 9999999999))

def generate_random_date():
  """Генерирует случайную дату рождения."""
  start_date = datetime.date(1950, 1, 1)
  end_date = datetime.date(2005, 12, 31)
  return start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))

# Создаем пустой список для хранения данных клиентов
clients = []

# Генерируем 100 записей о клиентах
for i in range(100):
  # Генерируем случайный пол
  gender = random.choice(["мужской", "женский"])
  # Генерируем случайные имя, фамилию, отчество
  first_name, last_name, patronymic_name = generate_random_name(gender)
  # Генерируем случайный ИНН
  inn = generate_random_inn()
  # Генерируем случайную дату рождения
  date_of_birth = generate_random_date()
  # Создаем словарь с данными клиента
  client = {
    "Номер счета": i+1,
    "Фамилия": last_name,
    "Имя": first_name,
    "Отчество": patronymic_name,
    "Дата рождения": date_of_birth,
    "ИНН": inn,
    "ФИО ответственного": "Ответственный {}".format(i+1),
    "Статус": "Не в работе"
  }
  # Добавляем словарь с данными клиента в список clients
  clients.append(client)

# Выводим список клиентов на экран
for client in clients:
  print(client)

 #Можно сохранить полученные данные в файл (например, в формате CSV)
for client in clients:
   with open("clients.csv", "a") as file:
     file.write("{},{},{},{},{},{},{},{}\n".format(
       client["Номер счета"],
       client["Фамилия"],
       client["Имя"],
       client["Отчество"],
       client["Дата рождения"],
       client["ИНН"],
       client["ФИО ответственного"],
       client["Статус"]
     ))
