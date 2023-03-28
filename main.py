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
    while True:
        try:
            all_ntd, all_ntd_for_table = parse_all_ntd.get_ntd(URL_START_PAGE_OF_NTD)
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка ссылки на страницу НТД. Ошибка {error}')
            break
        except requests.exceptions.ConnectionError as error:
            print(f'Ошибка сети. Ошибка {error}')
            time.sleep(1)
            continue
        break

    print(all_ntd)
    # print(f'Найдено стандартов (изменений): {len((all_ntd["tbl_contents"])}')
    with open(Path.joinpath(Path.cwd(), 'all_ntd_for_table.json'), 'w', encoding='utf-8') as json_file:
        json.dump(all_ntd_for_table, json_file, ensure_ascii=False, indent=4)
    with open(Path.joinpath(Path.cwd(), 'all_ntd.json'), 'w', encoding='utf-8') as json_file:
        json.dump(all_ntd, json_file, ensure_ascii=False, indent=4)

    # сохранение НТД в файл в табличном виде по формату в файле
    tpl = DocxTemplate('ntd_tpl.docx')
    tpl.render(all_ntd_for_table)
    tpl.save('ntd.docx')

    context = {}
    for table_col_number, ntd in enumerate(all_ntd):
        doc = DocxTemplate('ntd.docx')
        ntd_rich_text = RichText()
        ntd_rich_text.add(ntd['ntd_number'],url_id=doc.build_url_id(ntd['ntd_url']), color='#0000ff', underline=True)
        context[f'ntd{str(table_col_number+1)}'] = ntd_rich_text

    print(context)
    doc.render(context)
    doc.save('ntd.docx')


if __name__ == '__main__':
    main()
