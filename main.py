import argparse
import sys
import book
import parse_tululu_category
import json


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
    start_page_id = parser_args.start_id
    end_page_id = parser_args.end_id

    Path.cwd().joinpath(FILE_DIR).mkdir(parents=True, exist_ok=True)
    Path.cwd().joinpath(IMAGE_DIR).mkdir(parents=True, exist_ok=True)

    page_of_category_url = 'https://tululu.org/l55/'
    pages_number = 1
    books_urls = parse_tululu_category.get_books_urls(page_of_category_url, pages_number)
    print(books_urls)
    print(len(books_urls))

    # скачка книг с... по...
    # start_book_id = parser_args.start_book_id
    # end_book_id = parser_args.end_book_id
    # if start_book_id < 0 or end_book_id < 0:
    #     sys.exit('Неверно введены ID книг')
    # if start_book_id > end_book_id:
    #     start_book_id, end_book_id = end_book_id, start_book_id
    # print(f'Ищем книги с ID от {start_book_id} по {end_book_id}')

    books_informations = []
    for book_num, book_page_url in enumerate(books_urls):
        if book_num+1 > 100:
            break
        print(f'Скачиваем по ссылке № {book_num+1}')
        filepath, book_information = book.get_book(book_page_url)
        if filepath:
            print(f'Скачана книга: {filepath}')
            books_informations.append(book_information)

    print(f'Скачано книг: ', {len(books_informations)})

    with open(Path.cwd().joinpath('books_informations.json'), 'w', encoding='utf-8') as json_file:
        json.dump(books_informations, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
