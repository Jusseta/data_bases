from src.db_creator import create_db, save_to_db
from src.config import config
from src.db_manager import DBManager


def main():
    params = config()
    db_name = 'hh_vacancies'

    create_db(db_name, params)
    save_to_db(db_name, params)

    dbmanager = DBManager(db_name, params)

    print('Приветствую Вас в программе по поиску вакансий!\n')

    while True:
        move = int(input('Пожалуйста, выберите нужное Вам действие:\n'
                         '1 - Показать список компаний с количеством вакансий\n'
                         '2 - Показать список всех вакансий\n'
                         '3 - Показать среднюю ЗП по всем вакансиям\n'
                         '4 - Показать список вакансий с ЗП больше средней\n'
                         '5 - Найти определенные вакансии по ключевому слову\n'))

        if move == 1:
            dbmanager.get_companies_and_vacancies_count()
        elif move == 2:
            dbmanager.get_all_vacancies()
        elif move == 3:
            dbmanager.get_avg_salary()
        elif move == 4:
            dbmanager.get_vacancies_with_higher_salary()
        elif move == 5:
            word_input = str(input('Введите слово:\n'))
            dbmanager.get_vacancies_with_keyword(word_input)
        else:
            print('Нет такого действия\n')
            continue

        user = int(input('\nЖелаете продолжить?\n'
                         '1 - Продолжить\n'
                         'Любое другое число - Выход\n'))
        if user == 1:
            continue
        else:
            print('Всего хорошего!')
            exit()


if __name__ == "__main__":
    main()
