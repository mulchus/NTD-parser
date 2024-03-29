import parse_all_ntd
import parse_all_ntd_notifications
import parse_all_digests
import json
import time
import requests

from docxtpl import DocxTemplate, RichText
from pathlib import Path


URL_PAGE_OF_DIGEST = 'https://www.gostinfo.ru/WeeklyDigest/'
DIGEST_PAGE_NUMBERS = 127, 130

URL_START_PAGE_OF_NTD = 'https://protect.gost.ru/default.aspx?control=6&month=10&year=2023'

# URL_START_PAGE_OF_NTD_NOTIFICATIONS = 'http://webportalsrv.gost.ru/portal/UVED_2007st.nsf/wMain?OpenView'


def main():
    print(f'парсинг дайджестов по стандартизации и техническому регулированию из {URL_PAGE_OF_DIGEST}')
    print(f'№№ {DIGEST_PAGE_NUMBERS}')
    while True:
        try:
            all_digests = parse_all_digests.get_digests(URL_PAGE_OF_DIGEST, DIGEST_PAGE_NUMBERS)
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка ссылки на страницу дайджестов. Ошибка {error}')
            break
        except requests.exceptions.ConnectionError as error:
            print(f'Ошибка сети. Ошибка {error}')
            time.sleep(1)
            continue
        break
    print(f'Найдено дайджестов: {len(all_digests)}\n\n\n')


    print(f'парсинг утвержденных НТД на Х месяц из {URL_START_PAGE_OF_NTD}')
    while True:
        try:
            all_ntd, all_ntd_for_table, hidden_change_names = parse_all_ntd.get_ntd(URL_START_PAGE_OF_NTD)
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка ссылки на страницу НТД. Ошибка {error}')
            break
        except requests.exceptions.ConnectionError as error:
            print(f'Ошибка сети. Ошибка {error}')
            time.sleep(1)
            continue
        break

    print(f'Найдено стандартов (изменений): {len(all_ntd)}')
    print(f'Всего изменений со скрытым названием: {len(hidden_change_names)}\n\n\n')
    # with open(Path.joinpath(Path.cwd(), 'all_ntd_for_table.json'), 'w', encoding='utf-8') as json_file:
    #     json.dump(all_ntd_for_table, json_file, ensure_ascii=False, indent=4)
    # with open(Path.joinpath(Path.cwd(), 'all_ntd.json'), 'w', encoding='utf-8') as json_file:
    #     json.dump(all_ntd, json_file, ensure_ascii=False, indent=4)
    # сохранение в json названий изменений НТД со скрытыми названиями
    with open(Path.joinpath(Path.cwd(), 'hidden_change_names.json'), 'w', encoding='utf-8') as json_file:
        json.dump(hidden_change_names, json_file, ensure_ascii=False, indent=4)

    # сохранение НТД в файл в табличном виде по формату в файле
    tpl = DocxTemplate('ntd_tpl.docx')
    tpl.render(all_ntd_for_table)
    tpl.save('ntd.docx')

    context = {}
    doc = DocxTemplate('ntd.docx')
    for table_col_number, ntd in enumerate(all_ntd):
        ntd_rich_text = RichText()
        ntd_rich_text.add(ntd['ntd_number'], url_id=doc.build_url_id(ntd['ntd_url']), color='#0000ff', underline=True)
        context[f'ntd{str(table_col_number+1)}'] = ntd_rich_text
    doc.render(context)
    doc.save('ntd.docx')


    # print(f'парсинг уведомлений об утвержденых НТД на Х месяц из {URL_START_PAGE_OF_NTD_NOTIFICATIONS}')
    # while True:
    #     try:
    #         all_notifications, all_notifications_for_table = \
    #             parse_all_ntd_notifications.get_ntd_notifications(URL_START_PAGE_OF_NTD_NOTIFICATIONS)
    #     except requests.exceptions.HTTPError as error:
    #         print(f'Ошибка ссылки на страницу НТД. Ошибка {error}')
    #         break
    #     except requests.exceptions.ConnectionError as error:
    #         print(f'Ошибка сети. Ошибка {error}')
    #         time.sleep(1)
    #         continue
    #     break
    #
    # print(f'Найдено уведомлений стандартов: {len(all_notifications)}\n')
    # # with open(Path.joinpath(Path.cwd(), 'all_notifications_for_table.json'), 'w', encoding='utf-8') as json_file:
    # #     json.dump(all_notifications_for_table, json_file, ensure_ascii=False, indent=4)
    # # with open(Path.joinpath(Path.cwd(), 'all_notifications.json'), 'w', encoding='utf-8') as json_file:
    # #     json.dump(all_notifications, json_file, ensure_ascii=False, indent=4)
    #
    # # сохранение уведомлений об НТД в файл в табличном виде по формату в файле
    # tpl = DocxTemplate('ntd_tpl.docx')
    # tpl.render(all_notifications_for_table)
    # tpl.save('notifications.docx')
    #
    # context = {}
    # doc = DocxTemplate('notifications.docx')
    # for table_col_number, notification in enumerate(all_notifications):
    #     ntd_rich_text = RichText()
    #     ntd_rich_text.add(notification['notifications_public_date'],
    #                       url_id=doc.build_url_id(notification['notifications_url']), color='#0000ff', underline=True)
    #     context[f'ntd{str(table_col_number+1)}'] = ntd_rich_text
    # doc.render(context)
    # doc.save('notifications.docx')


if __name__ == '__main__':
    main()
