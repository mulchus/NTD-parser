import parse_all_ntd
import json
import time
import requests
from docxtpl import DocxTemplate, RichText


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

    ntd_count = len(all_ntd)
    print(f'Найдено стандартов (изменений): ', {ntd_count})
    with open(Path.joinpath(Path.cwd(), 'all_ntd.json'), 'w', encoding='utf-8') as json_file:
        json.dump(all_ntd, json_file, ensure_ascii=False, indent=4)

    # сохранение НТД в файл в табличном виде по формату в файле
    doc = DocxTemplate("ntd_tpl.docx")

    ntd_rich_text = []
    for ntd in all_ntd:
        ntd_rich_text = RichText()
        ntd_rich_text.add(ntd['ntd_number'],url_id=doc.build_url_id(ntd['ntd_url']))
        break
    context = {
        'example': ntd_rich_text
    }
    # print(ntd_rich_text)
    doc.render(context)
    doc.save('ntd.docx')


if __name__ == '__main__':
    main()
