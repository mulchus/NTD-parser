# Скрипт скачивания книг с сайта https://tululu.org/


## Запуск

Для запуска у вас уже должен быть установлен Python 3.

- Скачайте код
- Установите зависимости командой 
```
pip install -r requirements.txt
```
- Запустите скрипт командой 
```
python main.py [start_id] [end_id]
```
где:
[start_id] - начальный номер книги (по умолчанию = 1);

[end_id] - конечный номер книги (по умолчанию = 2).

При наличии книги в формате .txt она скачивается в папку ``Books``, создаваемой автоматически в папке по скриптом.

Имя файла - ID и название книги.

При наличии изображения к книге оно скачивается в папку ``Images``, создаваемой автоматически в папке по скриптом.

При отсутствии книги в формате txt или страницы с книгой выводится соответствующее сообщение.


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).