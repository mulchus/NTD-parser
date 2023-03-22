import requests
import functions
import time
import main


from bs4 import BeautifulSoup
from urllib import parse


def get_book(book_page_url):
    book_id = parse.urlsplit(book_page_url).path.replace('/', '').replace('b', '')
    book_file_basis_url = 'https://tululu.org/txt.php'
    filepath = ''
    book_information = ''
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
            imgpath = functions.download_image(book_information['img_scr'], main.IMAGE_DIR)
            book_information['img_scr'] = imgpath.replace('\\', '/')
        except requests.exceptions.HTTPError as error:
            if error.errno:
                print('Нет картинки.')
        except requests.exceptions.ConnectionError as error:
            print(f'Ошибка сети.\nОшибка {error}')
            time.sleep(1)
            continue

        if txt_book:
            filepath = functions.save_txt_file(txt_book, f'{book_id}.{book_information["title"]}',
                                               main.FILE_DIR)
            book_information['book_path'] = filepath.replace('\\', '/')
        break
    return filepath, book_information


def parse_book_page(page_content, book_page_url):
    splitresult = parse.urlsplit(book_page_url)
    site_url = parse.urlunsplit([splitresult.scheme, splitresult.netloc, '', '', ''])

    book_title = page_content.find('div', id="content").find('h1').text.split('::')[0].rstrip()

    book_author = page_content.find('body').find('div', id="content").find('h1').find('a').text

    book_genres = []
    if page_content.find('span', class_='d_book'):
        book_genres = [genre.text for genre in page_content.find('span', class_='d_book').find('b')
                       .find_next_siblings('a')]

    book_img_url = parse.urljoin(site_url, page_content.find('div', class_='bookimage').find('img')['src'])

    book_comments = []
    if page_content.find('div', class_='texts'):
        book_comments = [comment.text for comment in page_content.find('div', class_='texts')
                         .find_all_next('span', class_='black')]

    # book_description = page_content.find_all('table', class_='d_book')[1].find('td').text  #по ТЗ пока не используется

    book_information = {
        'title': book_title,
        'author': book_author,
        'img_scr': book_img_url,
        'book_path': '',
        'comments': book_comments,
        'genres': book_genres,
    }
    return book_information
