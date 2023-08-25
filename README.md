## Проект "Фудграм"

Проект представляет собой сайт, на котором пользователи могут публиковать свои рецепты, 
добавлять чужие рецепты в избранное и подписываться на публикации других авторов.
Помимо этого, пользователям доступен сервис "Список покупок", позволяющий создать список 
продуктов, которые нужно купить для приготовления выбранных блюд.


### Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```sh
git clone https://github.com/DaniilFedotov/foodgram-project-react.git
```

```sh
cd foodgram-project-react
```

Перейти в директорию с инфраструктурой:

```sh
cd infra
```

Создать файл .env:

```sh
touch .env
```

Заполнить файл .env в соответствии с примером .env.example, размещенным в директории:

```
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_NAME=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=django-insecure-l2#856c+o8k+h!ddpzuy^j3yx#$j*%*x6t5zhl+zzf1me28452
ALLOWED_HOSTS=127.0.0.1,localhost,backend,0.0.0.0:8000
```

Запустить контейнеры локально следующей командой:

```sh
sudo docker compose up --build
```

После запуска, в другом терминале копировать статику бэкенда внутри контейнера:

```sh
sudo docker compose exec backend python manage.py collectstatic
```

```sh
sudo docker compose exec backend cp -r /app/static/. /backend_static/static
```

Там же создать и выполнить миграции:

```sh
sudo docker compose exec backend python manage.py makemigrations
```

```sh
sudo docker compose exec backend python manage.py migrate
```

Там же создать суперпользователя:

```sh
sudo docker compose exec backend python manage.py createsuperuser
```

После этого нужно создать ингредиенты и теги войдя в админ-зону в роли суперпользователя:

```
http://localhost:8000/admin/
```

Затем проект станет доступен локально по адресу:

```
http://localhost:8000/
```