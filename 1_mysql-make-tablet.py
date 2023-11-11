import mysql.connector

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

# SQL запити для створення таблиць
create_tables_queries = [
    """
    CREATE TABLE Client (
        ClientID INT AUTO_INCREMENT PRIMARY KEY,
        TypeClient ENUM('відомство', 'фізична особа') NOT NULL,
        Address VARCHAR(255),
        LastName VARCHAR(255) NOT NULL,
        FirstName VARCHAR(255) NOT NULL,
        MiddleName VARCHAR(255)
    )
    """,
    """
    CREATE TABLE Tariff (
        TariffID INT AUTO_INCREMENT PRIMARY KEY,
        TypeCall VARCHAR(255) NOT NULL,
        CostMinCall DECIMAL(10, 2) NOT NULL
    )
    """,
    """
    CREATE TABLE Phone (
        PhoneNumber CHAR(13) NOT NULL PRIMARY KEY,
        ClientID INT,
        FOREIGN KEY (ClientID) REFERENCES Client(ClientID)
    )
    """,
    """
    CREATE TABLE Conversations (
        ConversationsID INT AUTO_INCREMENT PRIMARY KEY,
        ConversationsDate DATE NOT NULL,
        PhoneNumber CHAR(13),
        ConversationsTime INT NOT NULL,
        TariffID INT,
        FOREIGN KEY (PhoneNumber) REFERENCES Phone(PhoneNumber),
        FOREIGN KEY (TariffID) REFERENCES Tariff(TariffID)
    )
    """
]

# Виконання SQL запитів для створення таблиць
for query in create_tables_queries:
    cursor.execute(query)

# Закриття підключення
cursor.close()
connection.close()
connection.close()