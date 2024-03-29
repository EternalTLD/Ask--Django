# ASK
Проект представляет собой сайт с ответами на вопросы. Пользователи могут создавать, обновлять, удалять вопросы, а также оставлять ответы к другим вопросам. Реализована регистрация и аутентификация, а также возможность редактировать свой профиль. Пользователь может ставить лайк/дизлайк на вопрос/ответ. Когда пользователь получает ответ на свой вопрос или кто-то лайкает его вопрос/ответ, то ему приходит соответсвующее уведомление. Приходят как пуш-уведомления (на сайте), так и email-уведомления. Реализовано API с помощью Django Rest Framework. Развертывание проекта через Docker-compose.

## Стек технологий
- Django - фреймворк; 
- Django Channels - для работы с веб-сокетами;
- Django Rest Framework - для реализации API приложения;
- Docker - для развертывания приложения;
- PostgreSQL - база данных;
- Celery - отправка уведомлений;
- Flower - мониторинг задач Celery;
- Redis - кэширование данных и брокер собщений для Celery;
- JS, CSS, HTML, шаблонизатор Django - фронтенд.

## Установка
Для развертывания приложения необходим Docker.
```sh
git clone https://github.com/EternalTLD/Ask--Django.git
```
```sh
cd Ask--Django
```
```sh
docker-compose up --build
```
