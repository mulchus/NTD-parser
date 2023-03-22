import requests
import os.path
import pathvalidate


from urllib import parse


def get_page(page_url, payload=''):
    try:
        page = requests.get(page_url, params=payload)
        page.raise_for_status()
        check_for_redirect(page)
    except requests.exceptions.HTTPError as error:
        raise requests.exceptions.HTTPError(error)
    except requests.exceptions.ConnectionError as error:
        raise requests.exceptions.ConnectionError(error)
    return page


def check_for_redirect(book_page):
    if book_page.url == 'https://tululu.org/':
        raise requests.HTTPError('Err:01 - Нет информации на данной странице', book_page.request)


def download_image(img_url, folder='Images'):
    folder = pathvalidate.sanitize_filepath(folder)
    _, filename = os.path.split(parse.urlsplit(parse.unquote(img_url)).path)
    filepath = os.path.join(folder, filename)
    image = requests.get(img_url)
    image.raise_for_status()
    check_for_redirect(image)
    with open(filepath, 'wb') as file:
        file.write(image.content)
        return filepath


def save_txt_file(txt_book, filename, folder):
    folder = pathvalidate.sanitize_filepath(folder)
    filename = pathvalidate.sanitize_filename(filename)
    filepath = os.path.join(folder, f'{filename}.txt')
    with open(filepath, 'wb') as file:
        file.write(txt_book.content)
    return filepath
