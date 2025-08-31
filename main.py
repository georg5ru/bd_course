from api import HH_Api
from setup_db import create_database, create_tables, add_company, add_vacancy
from db_manager import DBManager
import psycopg2


def main():
    # Creates the database and tables for storing the scraped data.
    create_database()
    create_tables()

    # Establishes a connection to the newly created database.
    conn = psycopg2.connect(dbname='hh_vacancies', user='postgres', password='simplepassword123', host='localhost')

    # Employer IDs to fetch data for.
    employer_ids = [1455, 1740, 78638]

    for employer_id in employer_ids:
        # Fetches employer and vacancy data from the HH.ru API.
        employer_data = HH_Api.get_employer(employer_id)
        vacancies = HH_Api.get_vacancies(employer_id)

        # Adds the employer data to the database.
        company_id = add_company(conn, employer_data['name'], employer_data.get('description', ''), employer_data.get('vacancies_url', ''))

        # Adds each vacancy for the employer.
        for vacancy in vacancies:
            salary_info = vacancy.get('salary')
            salary = salary_info.get('from') if salary_info else None

            add_vacancy(conn, vacancy['name'], salary, vacancy.get('alternate_url'), company_id)

    db_manager = DBManager(dbname='hh_vacancies', user='postgres', password='simplepassword123')

    # Console menu for database interactions.
    print('Choose an action:')
    print('1: View number of vacancies by company')
    print('2: View all vacancies')
    print('3: View average salary')
    print('4: View vacancies with salary above average')
    print('5: Search vacancies by keyword')

    # Handles user input for the d esired action.
    number = input('Enter the action number: ')
    if number == '1':
        print(db_manager.get_companies_and_vacancies_count())
    elif number == '2':
        print(db_manager.get_all_vacancies())
    elif number == '3':
        print(db_manager.get_average_salary())
    elif number == '4':
        print(db_manager.get_vacancies_with_higher_salary())
    elif number == '5':
        keyword = input("Enter a keyword: ")
        print(db_manager.get_vacancies_with_keyword(keyword))

    conn.close()


if __name__ == '__main__':
    main()
