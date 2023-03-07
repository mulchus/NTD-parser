import requests
from pathlib import Path
from bs4 import BeautifulSoup


def main():

    # url = "https://dvmn.org/media/Requests_Python_Logo.png"
    # image = get_image(url).content
    # filename = Path(url).name
    # save_image(image, filename)
    #
    # url = "https://dvmn.org/filer/canonical/1542890876/16/"
    # response = get_image(url)
    # image_url = response.url
    # image = response.content
    # filename = Path(image_url).name
    # save_image(image, filename)

    file_dir = Path.cwd().joinpath('Books')
    file_dir.mkdir(parents=True, exist_ok=True)

    book_page_url_basis = 'https://tululu.org/b'

    for book_id in range(20000, 20005):
        book_page_url = f'{book_page_url_basis}{book_id}'
        save_book(book_page_url, file_dir)


def save_book(book_page_url, file_dir):
    basis_url = 'https://tululu.org/txt.php?id='
    page_title = ''

    reqs = requests.get(book_page_url)
    reqs.raise_for_status()
    soup = BeautifulSoup(reqs.text, 'html.parser')
    # get page title
    for title in soup.find_all('title'):
        page_title = title.get_text()

    book_id = Path(book_page_url).name[1:]
    txt_book_url = f'{basis_url}{book_id}'

    txt_book = requests.get(txt_book_url)
    txt_book.raise_for_status()
    # print(txt_book.headers)
    # print(txt_book.headers.values())
    if 'Content-Disposition' in txt_book.headers:
        if 'filename' in txt_book.headers['Content-Disposition']:
            with open(file_dir.joinpath(f'{page_title.split(",")[0]}.txt'), 'wb') as file:
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
