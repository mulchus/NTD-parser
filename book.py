import requests
import functions
import time
import main


from bs4 import BeautifulSoup
from urllib import parse


def get_book(book_id):
    book_page_url = f'https://tululu.org/b{book_id}'
    book_file_basis_url = 'https://tululu.org/txt.php'
    filepath = ''
    while True:
        try:
            book_page = functions.get_page(book_page_url)
        except requests.exceptions.HTTPError as error:
            if not error.errno:
                print(f'Неверная ссылка на страницу с книгой.\nОшибка {error}')
            break
        except requests.exceptions.ConnectionError as error:
            print(f'Ошибка сети.\nОшибка {error}')
            time.sleep(1)
            continue

        page_content = BeautifulSoup(book_page.text, 'lxml')

        try:
            txt_book = functions.get_page(book_file_basis_url, {'id': book_id})
        except requests.exceptions.HTTPError:
            print(f'Нет файлов книги.')
            break
        except requests.exceptions.ConnectionError as error:
            print(f'Ошибка сети.\nОшибка {error}')
            time.sleep(1)
            continue

        book_information = parse_book_page(page_content, book_page_url)

        try:
            functions.download_image(book_information['book_img_url'], main.IMAGE_DIR)
        except requests.exceptions.HTTPError as error:
            if error.errno:
                print('Нет картинки.')
        except requests.exceptions.ConnectionError as error:
            print(f'Ошибка сети.\nОшибка {error}')
            time.sleep(1)
            continue

        if txt_book:
            filepath = functions.save_txt_file(txt_book, f'{book_id}. {book_information["book_name"]}', main.FILE_DIR)
        break
    return filepath


def parse_book_page(page_content, book_page_url):
    splitresult = parse.urlsplit(book_page_url)
    site_url = parse.urlunsplit([splitresult.scheme, splitresult.netloc, '', '', ''])

    book_name = page_content.find('div', id="content").find('h1').text.split('::')[0].rstrip()

    book_author = page_content.find('body').find('div', id="content").find('h1').find('a').text

    book_genres = []
    if page_content.find('span', class_='d_book'):
        book_genres = [genre.text for genre in page_content.find('span', class_='d_book').find('b')
                       .find_next_siblings('a')]

    book_img_url = parse.urljoin(site_url, page_content.find('div', class_='bookimage').find('img')['src'])

    comments = []
    if page_content.find('div', class_='texts'):
        comments = [comment.text for comment in page_content.find('div', class_='texts')
                    .find_all_next('span', class_='black')]

    book_description = page_content.find_all('table', class_='d_book')[1].find('td').text

    about_book = {
        'book_name': book_name,
        'book_author': book_author,
        'book_genres': book_genres,
        'book_img_url': book_img_url,
        'book_description': book_description,
        'comments': comments
    }
    return about_book
