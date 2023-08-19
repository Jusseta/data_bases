import requests
import datetime


class ResponseError(Exception):
    def __init__(self):
        self.message = 'Проблема соединения с сервером'

    def __str__(self):
        return self.message


class HeadHunterAPI:
    """Формирование запроса на HeadHunter"""
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        self.params = {
                      'pages': 10,
                      'per_page': 100,
                      'only_with_salary': True
                      }
        self.employers = [2999230,  # P&G
                          39305,  # Gazprom
                          3529,  # Sber
                          5557093,  # e-Comet
                          9206033,  # G5 Games
                          9311920,  # DNS
                          5060211,  # Astra
                          955,  # Sogaz
                          55440,  # Melon FG
                          1740]  # Yandex

    def get_response(self):
        """Получение списка вакансий от данных работодателей"""
        data = []
        for employer in self.employers:
            response = requests.get(f"https://api.hh.ru/vacancies?employer_id={employer}",
                                    headers=self.header, params=self.params)
            if response.status_code != 200:
                raise ResponseError
            data.append(response.json()['items'])
        full_data = [x for l in data for x in l]
        return full_data

    def get_employers(self):
        employers = []
        for emp in self.get_response():
            employers.append({'employer_id': emp['employer']['id'],
                              'employer_name': emp['employer']['name']})
        emp_dict = {i['employer_id']: i for i in employers}
        return list(emp_dict.values())

    def get_vacancies(self):
        vacancies = []
        for vac in self.get_response():
            raw_date = vac['published_at']
            date = datetime.datetime.fromisoformat(raw_date).strftime('%Y-%m-%d')

            if vac['salary']['from'] and vac['salary']['from'] is not None:
                salary = vac['salary']['from']

            vacancies.append({'vacancy_id': vac['id'],
                              'vacancy_name': vac['name'],
                              'employer': vac['employer']['name'],
                              'salary_from': salary,
                              'published_date': date,
                              'url': vac['alternate_url']})
        return vacancies
