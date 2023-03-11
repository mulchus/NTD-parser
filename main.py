import os.path
import pathvalidate


import requests
from pathlib import Path
from bs4 import BeautifulSoup
import re


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

    file_dir = Path.cwd().joinpath('Books')
    file_dir.mkdir(parents=True, exist_ok=True)
    book_file_basis_url = 'https://tululu.org/txt.php?id='

    for book_id in range(1, 11):
        print(f'book_id = {book_id}')
        txt_book_url = f'{book_file_basis_url}{book_id}'
        # save_book(book_id, file_dir)
        download_txt(txt_book_url, f'{book_id}')


def delete_specchar(string):
    return re.sub(r'[\\|/!@#$"]', '', string)


def download_txt(txt_book_url, filename, folder='books/|\\'):
    # folder = delete_specchar(folder)
    # filename = delete_specchar(filename)
    folder = pathvalidate.sanitize_filepath(folder)
    filename = pathvalidate.sanitize_filename(filename)
    filepath = os.path.join(folder, f'{filename}.txt')

    print(filepath)

    txt_book = requests.get(txt_book_url)
    txt_book.raise_for_status()
    if 'Content-Disposition' in txt_book.headers:
        with open(filepath, 'wb') as file:
            file.write(txt_book.content)
    return filepath


def check_for_redirect(book_page):
    book_page.raise_for_status()
    if book_page.url == 'https://tululu.org/':
        try:
            raise requests.HTTPError('Error page', book_page.request)
        except requests.HTTPError as error:
            return error


def save_book(book_id, file_dir):

    book_file_basis_url = 'https://tululu.org/txt.php?id='

    book_page_url = f'https://tululu.org/b{book_id}'
    book_page = requests.get(book_page_url)
    if check_for_redirect(book_page):
        print('Книга не найдена')

    # book_id = Path(book_page_url).name[1:]
    txt_book_url = f'{book_file_basis_url}{book_id}'

    txt_book = requests.get(txt_book_url)
    txt_book.raise_for_status()
    if 'Content-Disposition' in txt_book.headers:
        # get page title
        page_content = BeautifulSoup(book_page.text, 'lxml')

        # page_title = page_content.find('head').find('title')
        # print(page_title.text)

        book_name = page_content.find('body').find('div', id="content").find('h1')
        print(book_name.text.split('::')[0].rstrip())

        book_author = page_content.find('body').find('div', id="content").find('h1').find('a')
        print(book_author.text)

        img_url = f"https://tululu.org{page_content.find('div', class_='bookimage').find('img')['src']}"
        print(img_url)

        book_description = page_content.find_all('table', class_='d_book')[1].find('td')
        print(book_description.text)

        # for title in page_content.find_all('title'):
        #     page_title = title.get_text()
        #     print(page_title)

        if 'filename' in txt_book.headers['Content-Disposition']:
            with open(file_dir.joinpath(f'{book_id}.txt'), 'wb') as file:
                file.write(txt_book.content)


def get_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


def save_image(image, filename):
    with open(filename, 'wb') as file:
        file.write(image)


if __name__ == '__main__':
    main()
