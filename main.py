import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

# Параметри підключення до бази даних
db_config = {
    "user": "root",
    "password": "mypassword",
    "host": "localhost",
    "database": "mydatabase",
    "port": 3306  # Змініть порт, якщо це не 3306
}

# Створення об'єкта підключення з використанням SQLAlchemy
engine = create_engine(f'mysql+mysqlconnector://{db_config["user"]}:{db_config["password"]}@{db_config["host"]}:{db_config["port"]}/{db_config["database"]}')

# Створення підключення
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Функція для виведення таблиці та її дані
def display_table_data(table_name):
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, engine)
    print(f"Таблиця '{table_name}':")
    print(df)
    print("\n")

# Список таблиць, які потрібно вивести
tables_to_display = ["Client", "Tariff", "Phone", "Conversations"]

for table in tables_to_display:
    display_table_data(table)

# Запит 1: Відобразити всіх клієнтів, які є фізичними особами. Відсортувати по прізвищу клієнта.
query1 = """
SELECT *
FROM Client
WHERE TypeClient = 'Фізична особа'
ORDER BY LastName
"""

# Виконання запиту 1
cursor.execute(query1)
result1 = cursor.fetchall()

# Створення DataFrame з результатами запиту
df1 = pd.DataFrame(result1, columns=['Код клієнта', 'Тип клієнта', 'Адреса', 'Прізвище', 'Ім*я', 'По батькові'])

print("Результат запиту 1:")
print(df1)


# Запит 2: Порахувати кількість клієнтів, які є фізичними особами, та кількість клієнтів, які є відомством.
query2 = """
SELECT TypeClient, COUNT(*) AS Count
FROM Client
GROUP BY TypeClient
"""

# Виконання запиту 2
cursor.execute(query2)
result2 = cursor.fetchall()

# Створення DataFrame з результатами запиту
df2 = pd.DataFrame(result2, columns=['Тип клієнта', 'Кількість'])

print(" ")
print("Результат запиту 2:")
print(df2)

# Запит 3: Порахувати вартість кожної розмови (запит з обчислювальним полем).
query3 = """
SELECT c.ConversationsID, c.ConversationsDate, c.PhoneNumber, c.ConversationsTime, t.CostMinCall,
       c.ConversationsTime * t.CostMinCall AS TotalCost
FROM Conversations c
JOIN Tariff t ON c.TariffID = t.TariffID
"""

# Виконання запиту 3
cursor.execute(query3)
result3 = cursor.fetchall()

# Створення DataFrame з результатами запиту
df3 = pd.DataFrame(result3, columns=['Код розм.', 'Дата розм.', 'Телефон', 'Час розм.', 'Ціна', 'Заг.ціна'])

print(" ")
print("Результат запиту 3:")
print(df3)

# Запит 4: Відобразити список всіх розмов з обраним типом дзвінка (запит з параметром).
selected_type_call = "Міжміський"  # Замініть це значення на обраний тип дзвінка

query3 = """
SELECT c.ConversationsID, c.ConversationsDate, c.PhoneNumber, c.ConversationsTime, t.CostMinCall, 
    c.ConversationsTime * t.CostMinCall AS TotalCost
FROM Conversations c
JOIN Tariff t ON c.TariffID = t.TariffID
WHERE t.TypeCall = %s
"""

# Виконання запиту 4 з параметром
cursor.execute(query3, (selected_type_call,))
result3 = cursor.fetchall()

# Створення DataFrame з результатами запиту
df3 = pd.DataFrame(result3, columns=['Код розм.', 'Дата розм.', 'Телефон', 'Час розм.', 'Ціна', 'Заг.ціна'])

print(" ")
print(f"Результат запиту 4'{selected_type_call}':")
print(df3)

# Запит 5: Порахувати загальну вартість всіх розмов для кожного клієнта (підсумковий запит).
query5 = """
SELECT cl.ClientID, SUM(conv.ConversationsTime * t.CostMinCall) AS TotalCost
FROM Conversations conv
JOIN Phone p ON conv.PhoneNumber = p.PhoneNumber
JOIN Client cl ON p.ClientID = cl.ClientID
JOIN Tariff t ON conv.TariffID = t.TariffID
GROUP BY cl.ClientID
"""
# Виконання запиту 5
cursor.execute(query5)
result5 = cursor.fetchall()

# Створення DataFrame з результатами запиту
df5 = pd.DataFrame(result5, columns=['Код клієнта', 'Загальна ціна'])

print(" ")
print("Результат запиту 5:")
print(df5)

# Запит 6: Порахувати кількість хвилин кожного типу дзвінків для кожного клієнта (перехресний запит).
query6 = """
SELECT cl.ClientID, t.TypeCall, SUM(conv.ConversationsTime) AS TotalMinutes
FROM Conversations conv
JOIN Phone p ON conv.PhoneNumber = p.PhoneNumber
JOIN Client cl ON p.ClientID = cl.ClientID
JOIN Tariff t ON conv.TariffID = t.TariffID
GROUP BY cl.ClientID, t.TypeCall
"""
# Виконання запиту 6
cursor.execute(query6)
result6 = cursor.fetchall()

# Створення DataFrame з результатами запиту
df6 = pd.DataFrame(result6, columns=['Код клієнта', 'Тип звінка', 'Загальний час'])

print(" ")
print("Результат запиту 6:")
print(df6)

# Закриття підключення
cursor.close()
connection.close()