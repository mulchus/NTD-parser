import os.path
import pathvalidate


import requests
from pathlib import Path
from bs4 import BeautifulSoup


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
        txt_book = requests.get(txt_book_url)
        txt_book.raise_for_status()

        book_page_url = f'https://tululu.org/b{book_id}'
        book_page = requests.get(book_page_url)
        if check_for_redirect(book_page):
            print('Книга не найдена')

        if 'Content-Disposition' in txt_book.headers:
            page_content = BeautifulSoup(book_page.text, 'lxml')

            # get page title
            # page_title = page_content.find('head').find('title')
            # print(page_title.text)

            book_name = page_content.find('body').find('div', id="content").find('h1').text.split('::')[0].rstrip()
            print(book_name)

            book_author = page_content.find('body').find('div', id="content").find('h1').find('a')
            print(book_author.text)

            img_url = f"https://tululu.org{page_content.find('div', class_='bookimage').find('img')['src']}"
            print(img_url)

            book_description = page_content.find_all('table', class_='d_book')[1].find('td')
            print(book_description.text)

            filepath = download_txt(txt_book, book_name)
            print(filepath)


def download_txt(txt_book, filename, folder='books/|\\'):
    folder = pathvalidate.sanitize_filepath(folder)
    filename = pathvalidate.sanitize_filename(filename)
    filepath = os.path.join(folder, f'{filename}.txt')
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


def get_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


def save_image(image, filename):
    with open(filename, 'wb') as file:
        file.write(image)


if __name__ == '__main__':
    main()
