import functions
import requests
import time

from bs4 import BeautifulSoup
from urllib import parse


def get_books_urls(page_of_category_url, parser_args):
    books_urls = []
    splitresult = parse.urlsplit(page_of_category_url)
    site_url = parse.urlunsplit([splitresult.scheme, splitresult.netloc, '', '', ''])
    last_page = (BeautifulSoup(functions.get_page(page_of_category_url).text, 'lxml')).select('a.npage')[-1].text
    if not parser_args.end_page:
        parser_args.end_page = int(last_page)

    for page in range(parser_args.start_page, parser_args.end_page+1):
        if page > int(last_page):
            print('Страницы исчерпаны')
            break
        current_page = parse.urljoin(page_of_category_url, str(page))
        while True:
            try:
                category_page = functions.get_page(current_page)
            except requests.exceptions.HTTPError:
                break
            except requests.exceptions.ConnectionError as error:
                print(f'Ошибка сети.\nОшибка {error}')
                time.sleep(1)
                continue

            category_content = BeautifulSoup(category_page.text, 'lxml')

            for table in category_content.select('div#content table'):
                book_url = parse.urljoin(site_url, table.select_one('a')['href'])
                books_urls.append(book_url)
            break
    return books_urls
