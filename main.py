import os.path
import pathvalidate
import requests
import argparse
import sys
import time


from urllib import parse
from pathlib import Path
from bs4 import BeautifulSoup


FILE_DIR = 'Books'
IMAGE_DIR = 'Images'


def main():
    book_parser = argparse.ArgumentParser(description='Скрипт скачивания книг с сайта https://tululu.org/')
    book_parser.add_argument(
        'start_book_id',
        nargs='?',
        default=1,
        help='начальный номер книги'
    )
    book_parser.add_argument(
        'end_book_id',
        nargs='?',
        default=2,
        help='конечный номер книги'
    )

    book_parser_args = book_parser.parse_args()
    start_book_id = int(book_parser_args.start_book_id)
    end_book_id = int(book_parser_args.end_book_id)
    if start_book_id < 0 or end_book_id < 0:
        sys.exit('Неверно введены ID книг')
    if start_book_id > end_book_id:
        start_book_id, end_book_id = end_book_id, start_book_id

    print(f'Ищем книги с ID от {start_book_id} по {end_book_id}')

    Path.cwd().joinpath(FILE_DIR).mkdir(parents=True, exist_ok=True)
    Path.cwd().joinpath(IMAGE_DIR).mkdir(parents=True, exist_ok=True)

    book_file_basis_url = 'https://tululu.org/txt.php'

    for book_id in range(start_book_id, end_book_id+1):
        print('\n', f'book_id = {book_id}')
        book_page_url = f'https://tululu.org/b{book_id}'
        while True:
            try:
                book_page = requests.get(book_page_url)
                book_page.raise_for_status()
                check_for_redirect(book_page)
            except requests.exceptions.HTTPError as error:
                if error.errno:
                    print(error.errno)
                else:
                    print(f'Неверная ссылка на страницу с книгой.\nОшибка {error}')
                break
            except requests.exceptions.ConnectionError as error:
                print(f'Ошибка сети.\nОшибка {error}')
                time.sleep(1)
            else:
                payload = {'id': book_id}
                try:
                    txt_book = requests.get(book_file_basis_url, params=payload)
                    txt_book.raise_for_status()
                    check_for_redirect(txt_book)
                except requests.exceptions.HTTPError as error:
                    if error.errno:
                        print('Нет файлов книги.')
                        break
                else:
                    page_content = BeautifulSoup(book_page.text, 'lxml')
                    book_information = parse_book_page(page_content)
                    download_image(book_information['book_img_url'], book_information['book_name'], IMAGE_DIR)
                    filepath = download_txt(txt_book, f'{book_id}. {book_information["book_name"]}', FILE_DIR)
                    print(f'Скачана книга: {filepath}')
                    break


def parse_book_page(page_content):
    book_name = page_content.find('div', id="content").find('h1').text.split('::')[0].rstrip()

    book_author = page_content.find('body').find('div', id="content").find('h1').find('a').text

    book_genres = []
    if page_content.find('span', class_='d_book'):
        book_genres = page_content.find('span', class_='d_book').find('b').find_next_siblings('a')
        book_genres = [genre.text for genre in book_genres]

    book_img_url = f"https://tululu.org{page_content.find('div', class_='bookimage').find('img')['src']}"

    comments = []
    if page_content.find('div', class_='texts'):
        comments = page_content.find('div', class_='texts').find_all_next('span', class_='black')
        comments = [comment.text for comment in comments]

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


def folder_filename_validate(folder='', filename=''):
    if folder:
        folder = pathvalidate.sanitize_filepath(folder)
    if filename:
        filename = pathvalidate.sanitize_filename(filename)
    return folder, filename


def download_txt(txt_book, filename, folder='Books'):
    folder, filename = folder_filename_validate(folder, filename)
    filepath = os.path.join(folder, f'{filename}.txt')
    with open(filepath, 'wb') as file:
        file.write(txt_book.content)
    return filepath


def download_image(img_url, filename, folder='Images'):
    folder, filename = folder_filename_validate(folder, filename)
    _, filename = os.path.split(parse.urlsplit(parse.unquote(img_url)).path)
    filepath = os.path.join(folder, filename)
    image = requests.get(img_url)
    with open(filepath, 'wb') as file:
        file.write(image.content)
    return filepath


def check_for_redirect(book_page):
    if book_page.url == 'https://tululu.org/':
        raise requests.HTTPError('Err:01 - Нет книги на этой странице', book_page.request)


if __name__ == '__main__':
    main()
