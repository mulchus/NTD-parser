import requests
from main import SEEKING_WORD_ROOTS

from bs4 import BeautifulSoup
from urllib import parse


def get_ntd(url_start_page_of_ntd):
    all_ntd = []
    all_ntd_for_table = {'tbl_contents':[]}
    splitresult = parse.urlsplit(url_start_page_of_ntd)
    site_url = parse.urlunsplit([splitresult.scheme, splitresult.netloc, '', '', ''])
    url_start_page_of_ntd_text = get_page(url_start_page_of_ntd, None).text
    soup = BeautifulSoup(url_start_page_of_ntd_text, 'lxml')
    last_page = int(soup.select('td.pages a')[-1].text)
    table_col_number = 1
    for page in range(0, last_page):
        current_page = url_start_page_of_ntd
        payload = {
            'page': page
        }
        page_of_ntds = get_page(current_page, payload)
        page_of_ntds_content = BeautifulSoup(page_of_ntds.text, 'lxml')

        for table in page_of_ntds_content.select('tr[bgcolor="#eeeeee"]'):
            ntd_url = parse.urljoin('https://protect.gost.ru/', table.select_one('td div a')['href'])
            ntd_number = table.select('td div[align="left"]')[0].text
            ntd_name = table.select('td div[align="left"]')[1].text
            if not ntd_name:
                page_of_izm_ntd = get_page(ntd_url, '')
                page_of_izm_ntd_content = BeautifulSoup(page_of_izm_ntd.text, 'lxml')
                ntd_name = page_of_izm_ntd_content.select('td[colspan="3"]')[-2].select_one('tr.first').select('td')[-1].text

            for root in SEEKING_WORD_ROOTS:
                if root in ntd_name.lower() or root in ntd_number.lower():

                    # результат в формате словаря
                    ntd = {
                        'ntd_url': ntd_url,
                        'ntd_number': ntd_number,
                        'ntd_name': ntd_name,
                    }

                    # результат в формате словаря списков для таблицы
                    ntd_for_table = {
                        'cols': ['{{r ntd'+str(table_col_number)+'}}', ntd_name]
                    }

                    all_ntd.append(ntd)
                    all_ntd_for_table['tbl_contents'].append(ntd_for_table)
                    table_col_number += 1
                    print(f'{ntd_number} - {ntd_name}')
                    break
            # break

    return all_ntd, all_ntd_for_table


def get_page(page_url, payload):
    page = requests.get(page_url, params=payload)
    page.raise_for_status()
    check_for_redirect(page)
    return page


def check_for_redirect(page):
    if page.url == 'https://protect.gost.ru/':
        raise requests.HTTPError('Err:01 - Нет информации на данной странице', page.request)
