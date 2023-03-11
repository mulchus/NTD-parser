import os.path
import pathvalidate
from urllib import parse


import requests
from pathlib import Path
from bs4 import BeautifulSoup


FILE_DIR = 'Books'
IMAGE_DIR = 'Images'


def main():

    # получение картинки по прямому адресу
    # url = "https://dvmn.org/media/Requests_Python_Logo.png"
    # image = get_image(url).content
    # filename = Path(url).name
    # save_image(image, filename)

    # получение картинки по косвенному адресуб в котором адрес
    # url = "https://dvmn.org/filer/canonical/1542890876/16/"
    # response = get_image(url)
    # image_url = response.url
    # image = response.content
    # filename = Path(image_url).name
    # save_image(image, filename)

    Path.cwd().joinpath(FILE_DIR).mkdir(parents=True, exist_ok=True)
    Path.cwd().joinpath(IMAGE_DIR).mkdir(parents=True, exist_ok=True)

    book_file_basis_url = 'https://tululu.org/txt.php?id='

    for book_id in range(5, 11):
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

            # get page title
            # page_title = page_content.find('head').find('title')
            # print(page_title.text)

            book_name = page_content.find('div', id="content").find('h1').text.split('::')[0].rstrip()
            print(book_name)

            if page_content.find('span', class_='d_book'):
                book_genres = page_content.find('span', class_='d_book').find('b').find_next_siblings('a')
                # print(book_genres)
                book_genres = [genre.text for genre in book_genres]
                print(book_genres)

            # book_author = page_content.find('body').find('div', id="content").find('h1').find('a')
            # print(book_author.text)

            img_url = f"https://tululu.org{page_content.find('div', class_='bookimage').find('img')['src']}"
            # print(img_url)
            # download_image(img_url, book_name, IMAGE_DIR)

            if page_content.find('div', class_='texts'):
                comments = page_content.find('div', class_='texts').find_all_next('span', class_='black')
                # for comment in comments:
                #     print(comment.text)

            # book_description = page_content.find_all('table', class_='d_book')[1].find('td')
            # if book_description.text:
            #     print(book_description.text)

            # filepath = download_txt(txt_book, f'{book_id}. {book_name}', FILE_DIR)
            # print(filepath)

        else:
            print('Нет файлов книги')


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


def get_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


def save_image(image, filename):
    with open(filename, 'wb') as file:
        file.write(image)


if __name__ == '__main__':
    main()
