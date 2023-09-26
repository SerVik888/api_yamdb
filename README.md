# Это пример его нужно будет
# api_yamdb
api_yamdb
# Проект на Django «...»

## Краткое описание проекта.

### При запуске проекта буду достнупны такие эндпоинты:
-- Пример --
- api/v1/users/ - адрес для работы с пользоваетлями\
`GET`, `POST`, `PUT`, `DELETE` Нужна авторизация

*Более подробное описание будет доступно в документации по адресу http://127.0.0.1:8000/redoc/ 
после запуска проекта.*

### Как запустить проект:

`git clone git@github.com:SerVik888/api_final_yatube.git` -> клонировать репозиторий

`cd api_final_yatube` -> перейти в репозиторий

* Если у вас Linux/macOS\
    `python3 -m venv env` -> создать виртуальное окружение\
    `source env/bin/activate` -> активировать виртуальное окружение\
    `python3 -m pip install --upgrade pip` -> обновить установщик\
    `pip install -r requirements.txt` -> установить зависимости из файла requirements.txt\
    `python3 manage.py migrate` -> выполнить миграции\
    `python3 manage.py createsuperuser` -> создать суперпользователя\
    `python3 manage.py runserver` -> запустить проект

* Если у вас windows\
    `python -m venv venv` -> создать виртуальное окружение\
    `source venv/Scripts/activate` -> активировать виртуальное окружение\
    `python -m pip install --upgrade pip` -> обновить установщик\
    `pip install -r requirements.txt` -> установить зависимости из файла requirements.txt\
    `python manage.py migrate` -> выполнить миграции\
    `python manage.py createsuperuser` -> создать суперпользователя\
    `python manage.py runserver` -> запустить проект

### Cписок используемых технологий

- Django
- pytest
- djangorestframework
- djangorestframework-simplejwt
- djoser


Авторы: Сафонов Сергей\
Почта: [sergey_safonov86@inbox.ru](mailto:sergey_safonov86@inbox.ru)