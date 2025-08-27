import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="my_db",
    user="my_user",
    password="my_secret"
)

try:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            date DATE NOT NULL,
            time TIME NOT NULL,
            details TEXT
        );
    ''')
    conn.commit()
    print("Подключение к базе данных установлено успешно!")
except psycopg2.OperationalError as e:
    print(f"Не удалось подключиться к базе данных: {e}")