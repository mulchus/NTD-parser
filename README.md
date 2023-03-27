# Скрипт получения списка и ссылок на новые нормативно-технические документы (НТД) с сайта Росстандарта https://protect.gost.ru/


## Настройки

Для запуска у вас уже должен быть установлен Python 3.

- Скачайте код
- Установите зависимости командой 
```
pip install -r requirements.txt
```

В файле main.py необходимо скорректировать некоторые константы под себя:

URL_START_PAGE_OF_NTD = 'https://protect.gost.ru/default.aspx?control=6&month=3&year=2023' 
(ссылка первую страницу стандартов за конкретный месяц)

WORD_ROOT_FILTER = ('','',''...) - список-фильтр корней слов для отбора НТД


## Запуск
- Запустите скрипт командой 
```
python main.py
```
Список всех найденных стандартов, с учетом фильтра корней слов, сохраняется в файле all_ntd.json


## Цели проекта

Код написан для работы в строительной отрасли в целях периодического мониторинга вновь принятых ГОСТ, ГОСТ Р и прочих.
