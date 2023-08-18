import psycopg2
from vacancies import HeadHunterAPI


def create_db(database_name: str, params: dict):
    """Создание базы данных и таблиц с нужными колонками в них"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE employers 
                (
                    id SERIAL PRIMARY KEY,
                    employer_id INTEGER,
                    employer_name VARCHAR(70) NOT NULL
                )
            """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies 
            (
                id SERIAL PRIMARY KEY,
                vacancy_name VARCHAR(200) NOT NULL,
                employer VARCHAR(100) NOT NULL,
                employer_id INT REFERENCES employers(id),
                salary_from INT NOT NULL,
                published_date TIMESTAMP,
                url TEXT
            )
        """)

    conn.commit()
    conn.close()


def save_to_db(database_name: str, params: dict):
    """Сохранение данных о работодателях и вакансиях в базу данных."""
    employers = HeadHunterAPI().get_employers()
    vacancies = HeadHunterAPI().get_vacancies()
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for emp in employers:
            cur.execute(
                """
                INSERT INTO employers (employer_id, employer_name) 
                VALUES (%s, %s)
                RETURNING id
                """,
                (emp['employer_id'], emp['employer_name'])
            )

        emp_id = cur.fetchone()[0]

        for vac in vacancies:
            cur.execute(
                """
                INSERT INTO vacancies (vacancy_name, employer, employer_id, 
                salary_from, published_date, url)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (vac['vacancy_name'], vac['employer'], emp_id, vac['salary_from'], vac['published_date'], vac['url'])
            )

    conn.commit()
    conn.close()
