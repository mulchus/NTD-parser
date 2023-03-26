import functions

from bs4 import BeautifulSoup
from urllib import parse


def get_books_urls(page_of_category_url, start_page, end_page):
    books_urls = []
    splitresult = parse.urlsplit(page_of_category_url)
    site_url = parse.urlunsplit([splitresult.scheme, splitresult.netloc, '', '', ''])
    page_of_category_url_text = functions.get_page(page_of_category_url).text
    soup = BeautifulSoup(page_of_category_url_text, 'lxml')
    last_page = int(soup.select('a.npage')[-1].text)
    if not end_page:
        end_page = last_page
    for page in range(start_page, min(end_page, last_page)+1):
        current_page = parse.urljoin(page_of_category_url, str(page))
        category_page = functions.get_page(current_page)
        category_content = BeautifulSoup(category_page.text, 'lxml')

        for table in category_content.select('div#content table'):
            book_url = parse.urljoin(site_url, table.select_one('a')['href'])
            books_urls.append(book_url)
    return books_urls
