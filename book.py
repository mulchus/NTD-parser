import functions
import main

from pathlib import Path
from bs4 import BeautifulSoup
from urllib import parse


def get_book(book_page_url, parser_args):
    book_id = parse.urlsplit(book_page_url).path.replace('/', '').replace('b', '')
    book_file_basis_url = 'https://tululu.org/txt.php'
    filepath = ''
    while True:
        book_page = functions.get_page(book_page_url)
        page_content = BeautifulSoup(book_page.text, 'lxml')
        book_information = parse_book_page(page_content, book_page_url)

        if not parser_args.skip_txt:
            txt_book = functions.get_page(book_file_basis_url, {'id': book_id})
            filepath = functions.save_txt_file(txt_book, f'{book_id}.{book_information["title"]}',
                                               Path.joinpath(parser_args.dest_folder, main.FILE_DIR))
            book_information['book_path'] = filepath.replace('\\', '/')

        if not parser_args.skip_imgs:
            imgpath = functions.download_image(book_information['img_scr'],
                                               Path.joinpath(parser_args.dest_folder, main.IMAGE_DIR))
            book_information['img_scr'] = imgpath.replace('\\', '/')

        break
    return filepath, book_information


def parse_book_page(page_content, book_page_url):
    splitresult = parse.urlsplit(book_page_url)
    site_url = parse.urlunsplit([splitresult.scheme, splitresult.netloc, '', '', ''])

    book_title = page_content.select_one('div#content h1').text.split('::')[0].rstrip()
    book_author = page_content.select_one('body div#content h1 a').text

    book_genres = []
    if page_content.select_one('span.d_book'):
        book_genres = [genre.text for genre in page_content.select('span.d_book a')]

    book_img_url = parse.urljoin(site_url, page_content.select_one('div.bookimage a img')['src'])

    book_comments = []
    if page_content.select_one('div.texts'):
        book_comments = [comment.text for comment in page_content.select('div.texts span.black')]

    book_information = {
        'title': book_title,
        'author': book_author,
        'img_scr': book_img_url,
        'book_path': '',
        'comments': book_comments,
        'genres': book_genres,
    }
    return book_information
