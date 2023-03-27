import parse_all_ntd
import json
import time
import requests

from pathlib import Path


URL_START_PAGE_OF_NTD = 'https://protect.gost.ru/default.aspx?control=6&month=3&year=2023'
URL_START_PAGE_OF_NTD_PROJECT = ''
WORD_ROOT_FILTER = ('геодез', 'геолог', 'эколог', 'гидромет', 'почв', 'проект', 'изыск', 'GPS', )



def main():

    # парсинг утвержденных НТД на Х месяц из URL_START_PAGE_OF_NTD
    all_ntd = []
    while True:
        try:
            all_ntd = parse_all_ntd.get_ntd(URL_START_PAGE_OF_NTD)
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка ссылки на страницу НТД. Ошибка {error}')
            break
        except requests.exceptions.ConnectionError as error:
            print(f'Ошибка сети. Ошибка {error}')
            time.sleep(1)
            continue
        break

    print(f'Найдено стандартов (изменений): ', {len(all_ntd)})
    with open(Path.joinpath(Path.cwd(), 'all_ntd.json'), 'w', encoding='utf-8') as json_file:
        json.dump(all_ntd, json_file, ensure_ascii=False, indent=4)








if __name__ == '__main__':
    main()
