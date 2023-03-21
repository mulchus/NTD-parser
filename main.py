import argparse
import sys
import book
import parse_tululu_category

from pathlib import Path


FILE_DIR = 'Books'
IMAGE_DIR = 'Images'


def main():
    parser = argparse.ArgumentParser(description='Скрипт скачивания книг с сайта https://tululu.org/')
    parser.add_argument(
        'start_id',
        nargs='?',
        type=int,
        default=1,
        help='начальный номер книги'
    )
    parser.add_argument(
        'end_id',
        nargs='?',
        type=int,
        default=2,
        help='конечный номер книги'
    )

    parser_args = parser.parse_args()

    Path.cwd().joinpath(FILE_DIR).mkdir(parents=True, exist_ok=True)
    Path.cwd().joinpath(IMAGE_DIR).mkdir(parents=True, exist_ok=True)

    start_page_id = parser_args.start_id
    end_page_id = parser_args.end_id

    page_of_category_url = 'https://tululu.org/l55/'
    parse_tululu_category.find_books_urls(page_of_category_url)


    # скачка книг с... по...
    # start_book_id = parser_args.start_book_id
    # end_book_id = parser_args.end_book_id
    # if start_book_id < 0 or end_book_id < 0:
    #     sys.exit('Неверно введены ID книг')
    # if start_book_id > end_book_id:
    #     start_book_id, end_book_id = end_book_id, start_book_id
    # print(f'Ищем книги с ID от {start_book_id} по {end_book_id}')

    # for book_id in range(start_book_id, end_book_id+1):
    #     print('\n', f'book_id = {book_id}')
    #     filepath = book.get_book(book_id)
    #     if filepath:
    #         print(f'Скачана книга: {filepath}')


if __name__ == '__main__':
    main()
