import psycopg2


class DBManager:
    """Подключение к базе данных и работа с ней"""
    def __init__(self, db_name: str, params: dict):
        self.db_name = db_name
        self.params = params
        self.conn = psycopg2.connect(dbname=self.db_name, **self.params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        with self.conn.cursor() as cur:
            cur.execute("""
                            SELECT employer, COUNT(vacancy_name)
                            FROM vacancies
                            GROUP BY employer
                      """
                        )
            result = cur.fetchall()

            for emp, count in result:
                print(f'Вакансий компании {emp}: {count}')

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и
        зарплаты и ссылки на вакансию"""
        with self.conn.cursor() as cur:
            cur.execute("""
                        SELECT employer, vacancy_name, salary_from, url 
                        FROM vacancies                            
                        """
                        )
            vacs = cur.fetchall()

            for vacancy, employer, salary, url in vacs:
                print(f"Компания: {employer}, вакансия: {vacancy}, зарплата: {salary}, ссылка: {url}")

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute("""                            
                        SELECT ROUND(AVG(salary_from)) FROM vacancies
                        """
                        )
            avg_salary = cur.fetchone()[0]
            print(f"Средняя зарплата: {avg_salary} руб.")

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute("""
                        SELECT employer, vacancy_name, salary_from, url 
                        FROM vacancies
                        WHERE salary_from > (SELECT ROUND(AVG(salary_from)) FROM vacancies)
                        """,
                        )
            vacs = cur.fetchall()

            for vacancy, employer, salary, url in vacs:
                print(f"Компания: {employer}, вакансия: {vacancy}, зарплата: {salary}, ссылка: {url}")

    def get_vacancies_with_keyword(self, keyword: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова,
        keyword - искомое слово в названии вакансии"""
        with self.conn.cursor() as cur:
            cur.execute(f"""
                        SELECT employer, vacancy_name, salary_from, url 
                        FROM vacancies      
                        WHERE LOWER(vacancy_name) LIKE '%{keyword.lower()}%'                                         
                        """
                        )
            vacs = cur.fetchall()

            for employer, vacancy, salary, url in vacs:
                print(f"Компания: {employer}, вакансия: {vacancy}, зарплата: {salary}, ссылка: {url}")

        cur.close()
