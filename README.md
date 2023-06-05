![foodgram Actions Status](https://github.com/VladislavYar/foodgram-project-react/actions/workflows/foodgram.yml/badge.svg)
# Адресс: ```158.160.17.165```
# mail admin: ```cool.reviewer@yandex.meow```
# password admin: ```python2022```
## Описание
Проект Foodgram представляет из себя платформу для сбора рецептов от пользователей, с возможность добавление
в избранное, список покупок, а так же скачивание PDF-файла c необходимыми ингредиентами для блюд.

## Шаблон наполнения env-файла(так же аналогично для Secrets Actions)
- DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
- DB_NAME=postgres # имя базы данных
- POSTGRES_USER=postgres # логин для подключения к базе данных
- POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
- DB_HOST=db # название сервиса (контейнера)
- DB_PORT=5432 # порт для подключения к БД 

## Шаблон наполнения Secrets Actions
Обратите внимание что в проекте имеется CI/CD(GitHub Actions)
- DOCKER_USERNAME=<ваш_username_dockerhub>
- DOCKER_PASSWORD=<ваш_пароль_dockerhub>
- HOST=<IP-адрес_вашего_сервера>
- USER=<имя_пользователя_для_подключения_к_серверу>
- SSH_KEY=<ssh-ключ_пользователя_для_подключения_к_серверу>
- PASSPHRASE=<фраза-пароль_для_доступа_к_ssh-ключу> # если такой имеется
- TELEGRAM_TO=<ID-аккаунта>
- TELEGRAM_TOKEN=<токен_бота>

## Как запустить проект:

В терминале, перейдите в каталог, в который будет загружаться приложение:
```
cd 
```
Клонируйте репозиторий:
```
git clone git@github.com:VladislavYar/foodgram-project-react.git
```
### На данном этапе создайте env-файл по шаблону из раздела выше

Перейдите в каталог конфигурации nginx и поменяйте данные поля server_name в файле default.conf на IP(домен) Вашего сервера:
```
cd foodgram-project-react/infra/nginx/
sudo nano default.conf
```

Далее перейдите в папку инфраструктуры:
```
cd ..
```
Запустите docker-compose командой:
```
docker-compose up -d
```
Выпоните миграции:
```
docker-compose exec web python manage.py makemigrations app
docker-compose exec web python manage.py makemigrations users
docker-compose exec web python manage.py migrate
```
### Заполнить базу данных начальными данными (из резервной копии) можно по инструкции раздела ниже.

Создайте суперюзера (логин\почта\пароль):
```
docker-compose exec web python manage.py createsuperuser
```
Соберите статические файлы:
```
docker-compose exec web python manage.py collectstatic --no-input 
```
Теперь проект доступен по адресу http://"IP(домен) Вашего сервера"/.

Остановить и удалить контейнеры, оставив образы:
```
docker-compose down -v
```
### Команды для заполнения базы данных
Создать дамп (резервную копию) базы данных "fixtures.json" можно следующей командой:
```
docker-compose exec web python manage.py dumpdata > fixtures.json
```
Далее команды по востановлению базы данных из резервной копии. Узнаем CONTAINER ID для контейнера:
```
docker container ls -a
```
Копируем файл "fixtures.json" с фикстурами в контейнер:
```
docker cp fixtures.json <CONTAINER ID>:/app
```
Применяем фикстуры:
```
docker-compose exec web python manage.py loaddata fixtures.json
```
Удаляем файл "fixtures.json" из контейнера:
```
docker exec -it <CONTAINER ID> bash
rm fixtures.json
exit
```

## Пользовательские роли
- Аноним — может просматривать рецепты, доступна регистрация.
- Аутентифицированный пользователь — может просматривать, создавать, редактировать и удалять рецепты, добавлять в избранное и список покупок,
скачивать PDF-файл c необходимыми игредиентами для блюд.
- Администратор (admin) — полные права на управление всем контентом проекта.


### Регистрация нового пользователя

Method:POST `/api/users/`
```
{
"email": "vpupkin@yandex.ru",
"username": "vasya.pupkin",
"first_name": "Вася",
"last_name": "Пупкин",
"password": "Qwerty123"
}
```

### Получение токена:
Method:POST `/api/auth/token/login/`
```
{
"password": "string",
"email": "string"
}
```

### Удаление токена:
Method:POST `/api/auth/token/logout/`
```

```

### Изменение пароля:
Method:POST `/api/users/set_password/`
```
{
"new_password": "string",
"current_password": "string"
}
```

### Получение текущего пользователя.
Method:GET `/api/users/me/`

### Получение списка всех пользователей.
Method:GET `/api/users/`

### Получение определенного пользователя.
Method:GET `/api/users/{id}/`

### Получить список всех тегов:
Method:GET `/api/tags/`

### Получение определенного тега:
Method:GET `/api/tags/{id}/`

### Получить список всех ингредиентов:
Method:GET `/api/ingredients/`

### Получение определенного ингредиента:
Method:GET `/api/ingredients/{id}/`

### Получение списка всех рецептов:
Method:GET `/api/recipes/`

### Добавление рецепта:
Method:POST `/api/recipes/`
```
{
"ingredients": [
{
"id": 1123,
"amount": 10
}
],
"tags": [
1,
2
],
"image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
"name": "string",
"text": "string",
"cooking_time": 1
}
```

### Получение информации о рецепте:
Method:GET `/api/recipes/{id}/`

### Обновление информации о рецепте:
Method:PATCH `/api/recipes/{id}/`
```
{
"ingredients": [
{
"id": 1123,
"amount": 10
}
],
"tags": [
1,
2
],
"image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
"name": "string",
"text": "string",
"cooking_time": 1
}
```

### Удаление рецепта:
Method:DELETE `/api/recipes/{id}/`

### Скачать список покупок:
Method:GET `/api/recipes/download_shopping_cart/`

### Добавить рецепт в список покупок:
Method:POST `/api/recipes/{id}/shopping_cart/`

### Удалить рецепт из списка покупок:
Method:DELETE `/api/recipes/{id}/shopping_cart/`

### Добавить рецепт в избранное:
Method:POST `/api/recipes/{id}/favorite/`

### Удалить рецепт из избранного:
Method:DELETE `/api/recipes/{id}/favorite/`

### Подписки пользователя:
Method:GET `/api/users/subscriptions/`

### Подписаться на пользователя:
Method:POST `/api/users/{id}/subscribe/`

### Отписаться от пользователя:
Method:DELETE `/api/users/{id}/subscribe/`

