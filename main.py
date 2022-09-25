import psycopg2


def create_clietns_table(cursor):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(40) NOT NULL,
        last_name VARCHAR(40) NOT NULL,
        email TEXT UNIQUE NOT NULL
    );
    """)

def create_phones_table(cursor):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phones(
        client_id INT NOT NULL,
        phone BIGINT UNIQUE,
        PRIMARY KEY (client_id, phone),
        CONSTRAINT my_fk FOREIGN KEY (client_id)
        REFERENCES clients(id)
        ON DELETE CASCADE
    );
    """)

def add_client(cursor, first_name, last_name, email):
    cur.execute("""
    INSERT INTO clients(first_name, last_name, email) VALUES(%s, %s, %s);
    """, (first_name, last_name, email))

def add_phone(cursor, client_id, phone):
    cur.execute("""
        INSERT INTO phones(client_id, phone) VALUES(%s, %s);
        """, (client_id, phone))

def change_client(cursor, client_id, first_name=None, last_name=None, email=None):
    cur.execute("""
        UPDATE clients SET first_name=%s, last_name=%s, email=%s WHERE id=%s;
        """, (first_name, last_name, email, client_id))

def del_phone(cursor, client_id, phone):
    cur.execute("""
        DELETE from phones WHERE client_id=%s AND phone=%s;
        """, (client_id, phone))

def delete_client(cursor, client_id):
    cur.execute("""
        DELETE from clients WHERE id=%s;
        """, (client_id,))



def find_client(cursor, first_name=None, last_name=None, email=None, phone=None) :
    cur.execute("""
        SELECT first_name, last_name, email, phone
        FROM clients c
        JOIN phones p on p.client_id = c.id
        WHERE first_name = %s or last_name = %s or email = %s or phone = %s;
        """, (first_name, last_name, email, phone))
    print(cursor.fetchall())


with psycopg2.connect(database='test_db', user='postgres', password='123') as conn:
    with conn.cursor() as cur:
        create_clietns_table(cur)

        create_phones_table(cur)

        add_phone(cur, 1, 9011234567)

        add_client(cur, "Ivan", "Ivanov", "ivanov@mail.ru")

        change_client(cur, first_name='Petr', last_name='Petrov', email='hello@mail.ru', client_id=1)

        del_phone(cur, 1, 9011234567)

        delete_client(cur, '1')

        find_client(cur, phone=9011234567)

