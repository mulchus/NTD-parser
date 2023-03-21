import functions
import requests
import time


from bs4 import BeautifulSoup
from urllib import parse


def find_books_urls(page_of_category_url):
    splitresult = parse.urlsplit(page_of_category_url)
    site_url = parse.urlunsplit([splitresult.scheme, splitresult.netloc, '', '', ''])
    last_page = (BeautifulSoup(functions.get_page(page_of_category_url).text, 'lxml')).find_all('a',
                                                                                                class_='npage')[-1].text
    for page in range(0, 10):
        if page > int(last_page):
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

            for table in category_content.find('div', id='content').find_all('table'):
                book_url_2 = parse.urljoin(site_url, table.find('a')['href'])
                print(book_url_2)
            break
