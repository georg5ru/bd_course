import psycopg2

class DBManager:
    def __init__(self, dbname, user, password, host="localhost"):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        self.cursor.execute("""
            SELECT companies.name, COUNT(vacancies.id) AS vacancies_count
            FROM companies
            LEFT JOIN vacancies ON companies.id = vacancies.company_id
            GROUP BY companies.name
        """)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        self.cursor.execute("""
            SELECT companies.name, vacancies.title, vacancies.url
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.id;
        """)
        return self.cursor.fetchall()

    def get_average_salary(self):
        self.cursor.execute("SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL;")
        result = self.cursor.fetchone()
        return result[0] if result[0] else 0

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_average_salary()
        self.cursor.execute("""
            SELECT title, salary, url
            FROM vacancies
            WHERE salary > %s AND salary IS NOT NULL;
        """, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        self.cursor.execute("""
            SELECT title, salary, url
            FROM vacancies
            WHERE title ILIKE %s AND salary IS NOT NULL;
        """, (f'%{keyword}%',))
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()