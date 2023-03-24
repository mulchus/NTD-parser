import argparse
import book
import parse_tululu_category
import json

from pathlib import Path


FILE_DIR = 'Books'
IMAGE_DIR = 'Images'
PAGE_OF_CATEGORY_URL = 'https://tululu.org/l55/'


def main():
    parser = argparse.ArgumentParser(description='Скрипт скачивания книг с сайта https://tululu.org/')
    parser.add_argument(
        '--start_page',
        nargs='?',
        type=int,
        default=1,
        help='начальный номер книги'
    )
    parser.add_argument(
        '--end_page',
        nargs='?',
        type=int,
        default=0,
        help='конечный номер книги'
    )
    parser.add_argument(
        '--dest_folder',
        nargs='?',
        type=Path,
        default=Path.cwd(),
        help='путь к каталогу с результатами парсинга: картинкам, книгам, JSON'
    )
    parser.add_argument(
        '--skip_imgs',
        action="store_true",
        help='не скачивать картинки'
    )
    parser.add_argument(
        '--skip_txt',
        action="store_true",
        help='не скачивать книги'
    )
    parser.add_argument(
        '--json_path',
        nargs='?',
        type=Path,
        help='указать свой путь к *.json файлу с результатами'
    )

    parser_args = parser.parse_args()

    if not parser_args.skip_txt:
        Path.cwd().joinpath(parser_args.dest_folder, FILE_DIR).mkdir(parents=True, exist_ok=True)
    if not parser_args.skip_imgs:
        Path.cwd().joinpath(parser_args.dest_folder, IMAGE_DIR).mkdir(parents=True, exist_ok=True)
    if parser_args.skip_txt and parser_args.skip_imgs:
        parser_args.dest_folder.mkdir(parents=True, exist_ok=True)

    page_of_category_url = PAGE_OF_CATEGORY_URL
    books_urls = parse_tululu_category.get_books_urls(page_of_category_url,
                                                      parser_args.start_page, parser_args.end_page)

    books_informations = []
    for book_page_url in books_urls:
        filepath, book_information = book.get_book(book_page_url, parser_args)
        books_informations.append(book_information)
        if filepath:
            print(f'Скачана книга: {filepath}')

    if not parser_args.skip_txt:
        print(f'Скачано книг: ', {len(books_informations)})

    if not parser_args.json_path:
        parser_args.json_path = parser_args.dest_folder
    else:
        Path.joinpath(parser_args.json_path).mkdir(parents=True, exist_ok=True)

    with open(Path.joinpath(parser_args.json_path, 'books_informations.json'), 'w', encoding='utf-8') as json_file:
        json.dump(books_informations, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
