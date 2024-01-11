# ESportsBattle Site Aggregator
## Общие сведение
Данное приложение создано в рамках тестового задания для *"ООО 24H Софт"*. Необходимо было собирать информацию о расписании спортивных событий, в частности, новые матчи по дисциплинам CS2 и Футболу с сайта https://esportsbattle.com/, с возможностью расширения и расчета на большие объемы данных.
Всю информацию необходимо было записывать в Б/д Postgres. 

## Используемый стэк
### Python
* Quart (асинхронный аналог Flask)
* SQLAlchemy
* aiohttp
### Vue
* Vue2
* Vuetify

# Инструкция
## Docker
Для запуска проекта без головной боли (надеюсь) в первую очередь необходимо установить Docker и Docker-Compose. Более подробно про установку описано здесь https://www.docker.com/get-started/.

Узннать, корректно ли установлен Docker, можно при помощи ввода следующей комманды в консоли:
```
docker --version
```
В случае docker-compose:
```
docker-compose --version
```

## Git
Следующим шагом необходимо скачать проект. 
Сделать это можно при помощи сайта github.com при помощи кнопки Download ZIP в меню "<> Code" и затем распаковать на своем ПК:
![telegram-cloud-photo-size-2-5262561026665206724-y](https://github.com/RastaBoy/esportsbattle_aggregator/assets/37360266/c2563d72-c779-4f81-824d-d0bb00f45407)
Либо можно установить себе Git (подробнее здесь https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup) и в консоли ввести следующую команду:
```
git clone https://github.com/RastaBoy/esportsbattle_aggregator.git
```

## Настройки
### Важно! Это моё первое знакомство с docker-compose и вполне возможно, что настройки задаются по-другому.
В файле docker-compose.yml, в блоках "enviroment" задаются следующие переменные:
```
services:
  db:
    ...
    environment:
      - POSTGRES_PASSWORD=keepsecret # Пароль для доступа к Б/Д
      - POSTGRES_USER=esports # Имя пользоватебя для доступа к Б/Д
      - POSTGRES_DB=esportsbattle_matches # Название Б/Д
  app:
    ...
    environment:
      - POSTGRES_USERNAME=esports # Имя пользоватебя для доступа к Б/Д
      - POSTGRES_PASSWORD=keepsecret # Пароль для доступа к Б/Д
      - POSTGRES_HOST=db 
      - POSTGRES_PORT=5432
      - POSTGRES_DB_NAME=esportsbattle_matches # Название Б/Д
      - APP_PORT=11011 # Порт, на котором запускается сервер
      - UPDATE_TIMEOUT=60 # Задержка между обновлениями информации о грядущих матчах
```

## Запуск!
Итак, когда проект склонирован, а Docker установлен, можно приступить к запуску проекта. Для этого инициализируйте командную строку в папку с проектом и введите следующую команду:
```
docker-compose up
```

По-умолчанию проект запускается на порту 11011 и для того, чтобы ознакомиться с результатами работы приложения, в браузере необходимо перейти по ссылке http://127.0.0.1:11011/.
В случае, если всё прошло успешно, то по данному адресу должно отобразиться следующее:
![photo_2024-01-11_18-07-12](https://github.com/RastaBoy/esportsbattle_aggregator/assets/37360266/dbf6c103-1cd4-4b8c-93e7-661818961fc4)
