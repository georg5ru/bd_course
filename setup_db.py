import psycopg2

def create_database():
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='simplepassword123', host='localhost')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute('DROP DATABASE IF EXISTS hh_vacancies')
    cursor.execute('CREATE DATABASE hh_vacancies')
    conn.close()

def create_tables():
    conn = psycopg2.connect(dbname='hh_vacancies', user='postgres', password='simplepassword123', host='localhost')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE companies (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            vacancies_url VARCHAR(255)
        );
        CREATE TABLE vacancies (
            id SERIAL PRIMARY KEY,
            company_id INTEGER REFERENCES companies(id),
            title VARCHAR(255) NOT NULL,
            salary INTEGER,
            url VARCHAR(255)
        );
    """)
    conn.commit()
    conn.close()

def add_company(conn, name, description, vacancies_url):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO companies (name, description, vacancies_url)
        VALUES (%s, %s, %s) RETURNING id;
    """, (name, description, vacancies_url))
    conn.commit()
    return cursor.fetchone()[0]

def add_vacancy(conn, title, salary, url, company_id):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO vacancies (company_id, title, salary, url)
        VALUES (%s, %s, %s, %s);
    """, (company_id, title, salary, url))
    conn.commit()