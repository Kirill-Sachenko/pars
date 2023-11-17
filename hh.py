# main class="vacancy-serp-content"                                      все вакансии
# div class="vacancy-serp-item__layout"                                   1 вакансия
# div class="bloko-text"                                                  город
#  div class="bloko-header-section-2"                                           зп
# div class="bloko-link bloko-link_kind-tertiary"                           компания


import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json


keywords = ['python', 'Django', 'Flask']
# main_link = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'

# headers_gen = Headers(os = 'win', browser = 'Mircosoft Edge')

main_hh = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2')
main_hh_html = main_hh.text

main_soup = BeautifulSoup(main_hh_html, 'lxml')
vacancy_list = main_soup.find_all ('main', class_="vacancy-serp-content")


data = []

for vacancy in vacancy_list:
    link = vacancy.find('a', class_='bloko-link')['href']
    zp_tag = vacancy.find('span', class_="bloko-header-section-2")
    company_tag = vacancy.find('a', class_="bloko-link bloko-link_kind-tertiary")
    city_tag = vacancy.find('div', class_="bloko-text")
    if zp_tag:
        zp_tag = zp_tag.text.strip()
    else:
        zp_tag = 'Не указана'

    description = vacancy.find(class_='g-user-content').text
    if any(keyword.lower() in description.lower() for keyword in keywords):
        vacancy_info = {
            'link': link,
            'company': company_tag,
            'city': city_tag,
            'salary': zp_tag
        }
        data.append(vacancy_info)

with open('vacancies_from_hh.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)




