import os.path
import pathvalidate
import requests
import argparse
import sys


from urllib import parse
from pathlib import Path
from bs4 import BeautifulSoup


FILE_DIR = 'Books'
IMAGE_DIR = 'Images'


def main():
    award_parser = argparse.ArgumentParser(description='Скрипт скачивания книг с сайта https://tululu.org/')
    award_parser.add_argument(
        'start_id',
        nargs='?',
        default=1,
        help='начальный номер книги'
    )
    award_parser.add_argument(
        'end_id',
        nargs='?',
        default=2,
        help='конечный номер книги'
    )

    start_id = int(award_parser.parse_args().start_id)
    end_id = int(award_parser.parse_args().end_id)
    if start_id < 0 or end_id < 0:
        sys.exit('Неверно введены ID книг')
    if start_id > end_id:
        start_id, end_id = end_id, start_id

    print(f'Ищем книги с ID от {start_id} по {end_id}')

    Path.cwd().joinpath(FILE_DIR).mkdir(parents=True, exist_ok=True)
    Path.cwd().joinpath(IMAGE_DIR).mkdir(parents=True, exist_ok=True)

    book_file_basis_url = 'https://tululu.org/txt.php?id='

    for book_id in range(start_id, end_id+1):
        print('\n', f'book_id = {book_id}')
        txt_book_url = f'{book_file_basis_url}{book_id}'
        txt_book = requests.get(txt_book_url)
        txt_book.raise_for_status()

        book_page_url = f'https://tululu.org/b{book_id}'
        book_page = requests.get(book_page_url)

        if check_for_redirect(book_page):
            print('Книга не найдена')
            # print()
            continue

        if 'Content-Disposition' in txt_book.headers:
            page_content = BeautifulSoup(book_page.text, 'lxml')
            book_information = parse_book_page(page_content)
            download_image(book_information['book_img_url'], book_information['book_name'], IMAGE_DIR)
            filepath = download_txt(txt_book, f'{book_id}. {book_information["book_name"]}', FILE_DIR)
            print(f'Скачана книга: {filepath}')
        else:
            print('Нет файлов книги')


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

    book_information = {
        'book_name': book_name,
        'book_author': book_author,
        'book_genres': book_genres,
        'book_img_url': book_img_url,
        'book_description': book_description,
        'comments': comments
    }

    return book_information


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
    # _, file_ext = os.path.splitext(img_url)
    _, filename = os.path.split(parse.urlsplit(parse.unquote(img_url)).path)
    filepath = os.path.join(folder, filename)
    image = requests.get(img_url)
    with open(filepath, 'wb') as file:
        file.write(image.content)
    return filepath


def check_for_redirect(book_page):
    book_page.raise_for_status()
    if book_page.url == 'https://tululu.org/':
        try:
            raise requests.HTTPError('Error page', book_page.request)
        except requests.HTTPError as error:
            return error


if __name__ == '__main__':
    main()
