import psycopg2

conn = psycopg2.connect(database='sqlnettask4', user='postgres', password='123')
with conn.cursor() as cur:

    # Удаление таблицы
    cur.execute("""
    DROP TABLE clients_phone
    """)

    cur.execute("""
    DROP TABLE clients
    """)

    # 1.1. Функция, создающая структуру БД для ФИО + email (таблицы)
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
    cur.execute("""
            INSERT INTO clients(name, surname, email) VALUES('Рифат', 'Бахтиев', 'rifat@gmail.com') RETURNING id, name, surname, email;
            """)
    # print(cur.fetchone())

    # 3. Функция, позволяющая добавить телефон для существующего клиента
    cur.execute("""
            INSERT INTO clients_phone(clients_id, phone) VALUES(1, '8926') RETURNING id, clients_id, phone;
            """)
    # print(cur.fetchone())

    # 4.1. Функция позволяющая изменить данные о клиенте
    cur.execute("""
            UPDATE clients
            SET name = 'Иван', surname = 'Никифоров', email = 'ivan@gmail.com' RETURNING id, name, surname, email;
            """)
    # print(cur.fetchone())

    # 4.2. Функция позволяющая изменить данные о клиенте ТЕЛЕФОН
    cur.execute("""
            UPDATE clients_phone
            SET phone = '8928' RETURNING id, phone;
            """)
    # print(cur.fetchone())

    # 6.1. Функция, позволяющая удалить существующего клиента
    cur.execute("""
            DELETE FROM clients_phone
            WHERE id = 1
                """)

    # 6.2. Функция, позволяющая удалить существующего клиента
    cur.execute("""
            DELETE FROM clients
            WHERE id = 1
                """)

    # 7.1 Функция, позволяющая найти клиента по его данным(имени, фамилии, email - у)
    cur.execute("""
            SELECT clients.name, clients.surname, clients.email, clients_phone.phone FROM clients
            LEFT JOIN clients_phone on clients.id=clients_phone.clients_id
            where (name like 'Иван') AND (surname like 'Никифоров') AND (email like 'ivan@gmail.com')
            """)
    print(cur.fetchmany(3))

    # 7.2 Функция, позволяющая найти клиента по его данным(телефону)
    cur.execute("""
            SELECT clients.name, clients.surname, clients.email, clients_phone.phone FROM clients
            LEFT JOIN clients_phone on clients.id=clients_phone.clients_id
            where clients_phone.phone like '8928'
            """)
    # print(cur.fetchmany(3))

conn.close()