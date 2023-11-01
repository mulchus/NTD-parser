import requests
from common_tools import SEEKING_WORD_ROOTS

from bs4 import BeautifulSoup


def get_digests(url_page_of_digest, digest_page_numbers):
    all_digests = []
    first_page, end_page = digest_page_numbers
    for page in range(first_page, end_page+1):
        print (page)
        payload = {
            'digest': page
        }
        page_of_digests = get_page(url_page_of_digest, payload)
        page_of_digests_content = BeautifulSoup(page_of_digests.text, 'lxml')

        for digest_name in page_of_digests_content.select('p b'):
            for root in SEEKING_WORD_ROOTS:
                if root in digest_name.text.lower():
                    all_digests.append(digest_name.text)
                    print(digest_name.text)
                    break
    return all_digests


def get_page(page_url, payload):
    page = requests.get(page_url, params=payload)
    page.raise_for_status()
    return page
