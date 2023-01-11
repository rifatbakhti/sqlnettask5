import psycopg2

# 0 Удаление таблицы
def delete_db(cur):
    cur.execute("""
    DROP TABLE clients_phone
    """)

    cur.execute("""
    DROP TABLE clients
    """)

# 1.1. Функция, создающая структуру БД для ФИО + email (таблицы)
def create_db(cur):
    cur.execute("""
            CREATE TABLE IF NOT EXISTS clients(
                id SERIAL PRIMARY KEY,
                name VARCHAR(40) UNIQUE,
                surname VARCHAR(40) UNIQUE,
                email VARCHAR(40) UNIQUE
                );
                """)
    conn.commit()

# 1.2. Функция, создающая структуру БД для телефона (таблицы)
    cur.execute("""
             CREATE TABLE IF NOT EXISTS clients_phone(
                 id SERIAL PRIMARY KEY,
                 clients_id INTEGER not null references clients(id),
                 phone VARCHAR(40) UNIQUE
                 );
                 """)
    conn.commit()

# 2. Функция, позволяющая добавить нового клиента
def add_client(cur, name, surname, email, phones=None):
    cur.execute("""
                INSERT INTO clients (name, surname, email) 
                VALUES (%s, %s, %s);
                """, (name, surname, email))
    conn.commit()

# 3. Функция, позволяющая добавить телефон для существующего клиента
def add_phone(cur, client_id, phone):
    cur.execute("""
                INSERT INTO clients_phone(clients_id, phone) 
                VALUES(%s, %s);
                """, (client_id, phone))
    conn.commit()

# 4. Функция позволяющая изменить данные о клиенте
def change_client(cur, client_id, name=None, surname=None, email=None, phones=None):
    cur.execute("""
            UPDATE clients
            SET name = %s, surname = %s, email = %s
            WHERE id = %s;
            """, (name, surname, email, client_id))

    cur.execute("""
            UPDATE clients_phone
            SET phone = %s
            WHERE id = %s;
            """, (phones, client_id))

# 5. Функция, позволяющая удалить телефон
def delete_phone(cur, client_id, phone):
    cur.execute("""
            DELETE FROM clients_phone
            WHERE id = %s and phone = %s;
                """, (client_id, phone))

# 6. Функция, позволяющая удалить существующего клиента
def delete_client(cur, client_id):
    cur.execute("""
            DELETE FROM clients
            WHERE id = %s;
                """, (client_id))

# 7. Функция, позволяющая найти клиента по его данным
def find_client(conn, name=None, surname=None, email=None, phone=None):
    cur.execute("""
                SELECT clients.name, clients.surname, clients.email, clients_phone.phone FROM clients
                LEFT JOIN clients_phone on clients.id=clients_phone.clients_id
                where (name like %s) OR (surname like %s) OR (email like %s) OR (phone like %s)
                """, (name, surname, email, phone))
    print(cur.fetchmany(3))

conn = psycopg2.connect(database='sqlnettask4', user='postgres', password='123')
with conn.cursor() as cur:

    delete_db(cur)
    create_db(cur)
    add_client(cur, 'Рифат', 'Бахтиев', 'rifat@gmail.com')
    add_phone(cur, 1, '8926')
    change_client(cur, 1, "Иван", "Иванов", "ivan@gmail.com", "8999")
    delete_phone(cur, 1, "8999")
    delete_client(cur, '1')
    find_client(cur, "Иван", "")