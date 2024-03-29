from common_tools import SEEKING_WORD_ROOTS, get_page
from bs4 import BeautifulSoup
from urllib import parse


def get_ntd_notifications(url_start_page_of_ntd_notifications):
    all_notifications = []
    all_notifications_for_table = {'tbl_contents': []}
    start_page_of_ntd_notifications = get_page(url_start_page_of_ntd_notifications, None).text
    start_page_content = BeautifulSoup(start_page_of_ntd_notifications, 'lxml')
    current_month = int(start_page_content.select_one('tr[valign="top"] td a').text.split('/')[0])
    print(f'Исследуем текущий месяц № {current_month} и предшествующий ему месяц.')
    # иначе - удалить в parse_all_ntd_notifications.py "if int(notifications.....[0]) < current_month" значение "-1"')

    ntd_notifications_first_in_page_number = 1
    table_col_number = 1
    while True:
        payload = {
            'Start': ntd_notifications_first_in_page_number
        }
        page_of_notifications = get_page(url_start_page_of_ntd_notifications, payload)
        page_of_notifications_content = BeautifulSoup(page_of_notifications.text, 'lxml')

        for table_row in page_of_notifications_content.select('tr[valign="top"]'):
            notifications_public_date = table_row.select_one('td a').text

            # проверка даты на предыдущий месяц и возврат при True
            # !! Если необходимо исследовать и за прошлый месяц - сделать "current_month - 1"
            if int(notifications_public_date.split('/')[0]) < current_month - 1: # - 1:
                return all_notifications, all_notifications_for_table

            notifications_url = parse.urljoin('http://webportalsrv.gost.ru/', table_row.select_one('td a')['href'])
            notifications_type = table_row.select('td')[1].text
            ntd_name = table_row.select('td')[2].text

            for root in SEEKING_WORD_ROOTS:
                if root in ntd_name.lower():

                    # результат в формате словаря
                    ntd = {
                        'notifications_public_date': notifications_public_date,
                        'notifications_url': notifications_url,
                        'notifications_type': notifications_type,
                        'ntd_name': ntd_name,
                    }

                    # результат в формате словаря списков для таблицы
                    notifications_for_table = {
                        'cols': ['{{r ntd'+str(table_col_number)+'}}', notifications_type, ntd_name]
                    }
                    all_notifications.append(ntd)
                    all_notifications_for_table['tbl_contents'].append(notifications_for_table)
                    table_col_number += 1
                    print(f'{notifications_public_date} - {ntd_name}')
                    break
        ntd_notifications_first_in_page_number += 29
