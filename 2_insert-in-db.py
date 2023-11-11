import mysql.connector
from datetime import datetime, timedelta

# Параметри підключення до бази даних
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "mypassword",
    "database": "mydatabase"
}

# Створення підключення
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()


# Додавання даних до таблиці Клієнт
client_data = [
    ("Відомство", "Радищева 3", "Черкашин", "Максим", "Юрійович"),
    ("Фізична особа", "Радищева 4", "Маслюк", "Олег", "Олегович"),
    ("Відомство", "Радищева 5", "Янович", "Євген", "Максимович"),
    ("Фізична особа", "Радищева 6", "Кочубей", "Богдан", "Богданович"),
    ("Відомство", "Радищева 7", "Саміщенко", "Павло", "Олександрович")
]

insert_client_query = """
INSERT INTO Client (TypeClient, Address, LastName, FirstName, MiddleName)
VALUES (%s, %s, %s, %s, %s)
"""

cursor.executemany(insert_client_query, client_data)

# Додавання даних до таблиці Тариф
tariff_data = [
    ("Внутрішній", 5),
    ("Міжміський", 10),
    ("Мобільний", 15)
]

insert_tariff_query = """
INSERT INTO Tariff (TypeCall, CostMinCall)
VALUES (%s, %s)
"""

cursor.executemany(insert_tariff_query, tariff_data)

# Додавання даних до таблиці Телефон
phone_data = [
    ("0500134543", 1),
    ("0662342344", 2),
    ("0955354353", 3),
    ("0501231233", 4),
    ("0962342344", 5),
    ("0951231313", 1),
    ("0662342424", 2)
]

insert_phone_query = """
INSERT INTO Phone (PhoneNumber, ClientID)
VALUES (%s, %s)
"""

cursor.executemany(insert_phone_query, phone_data)

# Додавання даних до таблиці Розмови

conversations_data = [
    ("2023-11-01", "0500134543", 15, 1),
    ("2023-11-02", "0662342344", 30, 2),
    ("2023-11-03", "0955354353", 10, 3),
    ("2023-11-04", "0501231233", 14, 1),
    ("2023-11-05", "0962342344", 11, 2),
    ("2023-11-06", "0951231313", 36, 3),
    ("2023-11-07", "0662342424", 90, 1),
    ("2023-11-08", "0500134543", 37, 2),
    ("2023-11-09", "0955354353", 33, 3),
    ("2023-11-10", "0951231313", 21, 1),
    ("2023-11-11", "0662342424", 45, 2),
    ("2023-11-12", "0955354353", 80, 3),
    ("2023-11-13", "0500134543", 1, 1),
    ("2023-11-14", "0951231313", 25, 2),
    ("2023-11-15", "0662342424", 10, 3),
    ("2023-11-16", "0662342344", 38, 1),
    ("2023-11-17", "0955354353", 45, 2),
    ("2023-11-18", "0500134543", 47, 3),
    ("2023-11-19", "0962342344", 12, 1),
    ("2023-11-20", "0955354353", 19, 2),
]

insert_conversations_query = """
INSERT INTO Conversations (ConversationsDate, PhoneNumber, ConversationsTime, TariffID)
VALUES (%s, %s, %s, %s)
"""

cursor.executemany(insert_conversations_query, conversations_data)

# Підтвердження змін та закриття підключення
connection.commit()
cursor.close()
connection.close()