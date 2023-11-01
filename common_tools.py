import requests


SEEKING_WORD_ROOTS = ('геодез', 'геолог', 'эколог', 'гидромет', 'почв', 'грунт', 'здани', 'сооружен', 'проект',
                      'изыск', 'репутац', 'градостр', 'город', 'gps', 'глонасс', 'cнип', 'сп ', 'сейсм',
                      'землетряс', 'земл', 'земн', 'обслед', 'строит', 'стандартизация', 'моделирован',
                      'беспилот', 'бпла', 'мерзлот', )


def get_page(page_url, payload):
    page = requests.get(page_url, params=payload)
    page.raise_for_status()
    check_for_redirect(page)
    return page


def check_for_redirect(page):
    if page.url == 'https://protect.gost.ru/':
        raise requests.HTTPError('Err:01 - Нет информации на данной странице', page.request)
