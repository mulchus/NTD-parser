import requests
import main

from bs4 import BeautifulSoup
from urllib import parse
from docxtpl import DocxTemplate, RichText


def get_ntd_notifications(url_start_page_of_ntd_notifications):
    all_notifications = []
    all_notifications_for_table = {'tbl_contents':[]}
    splitresult = parse.urlsplit(url_start_page_of_ntd_notifications)
    site_url = parse.urlunsplit([splitresult.scheme, splitresult.netloc, '', '', ''])
    start_page_of_ntd_notifications = get_page(url_start_page_of_ntd_notifications, None).text
    start_page_content = BeautifulSoup(start_page_of_ntd_notifications, 'lxml')
    current_month = int(start_page_content.select_one('tr[valign="top"] td a').text.split('/')[0])

    # doc = DocxTemplate('ntd_tpl.docx')
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
            if int(notifications_public_date.split('/')[0]) < current_month:
                return all_notifications, all_notifications_for_table

            notifications_url = parse.urljoin('http://webportalsrv.gost.ru/', table_row.select_one('td a')['href'])
            notifications_type = table_row.select('td')[1].text
            ntd_name = table_row.select('td')[2].text

            for root in main.SEEKING_WORD_ROOTS:
                if root in ntd_name.lower():

                    # результат в формате словаря
                    # ntd_rich = RichText(notifications_public_date, url_id=doc.build_url_id(notifications_url), color="#0000ff", underline=True)
                    ntd = {
                        'notifications_public_date': notifications_public_date,
                        # 'notifications_public_date': ntd_rich,
                        # 'notifications_public_date': f'RichText({notifications_public_date}, '
                        #                              f'url_id=doc.build_url_id({notifications_url}), '
                        #                              f'color="#0000ff", underline=True)',
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


def get_page(page_url, payload):
    page = requests.get(page_url, params=payload)
    page.raise_for_status()
    check_for_redirect(page)
    return page


def check_for_redirect(page):
    if page.url == 'https://protect.gost.ru/':
        raise requests.HTTPError('Err:01 - Нет информации на данной странице', page.request)
