# API_YAMDB

Проект API YAMDB - лучшее веяние этого лета в сфере сбора отзывов произведений.
Любые категории произведений («Книги», «Фильмы», «Музыка») и жанров
(«Сказка», «Рок» или «Артхаус»). И они легко расширяются: все ограничено только
фантазией администратора приложения.

Любой пользователь системы может написать развернутый отзыв для добавленных
произведений и поставить оценку. А еще есть классная возможность комментировать
чужие отзывы. Находим в себе дух критика и идём разносить ~~чужие~~
неправильные
мнения.

## Разработчики

- [Сергей Колтыгин](https://github.com/cmipro)

- [Александр Роль](https://github.com/RolAlek)

- [Илья Киселёв](https://github.com/welesik)

> Во время разработки ни один разработчик не пострадал

## Используемые технологии

Python 3.11 + Django 3.2 + DRF + SQLite3

## Установка и запуск

1. Клонируем репозиторий и переходим в него.

```
git clone https://github.com/cmipro/api_yamdb
cd api_yamdb
```

2. Создаем и активируем виртуальное окружение.

```
Unix:
python3 -m venv env
source env/bin/activate

Windows:
python -m venv env
source env/Scripts/activate
```

3. Устанавливаем зависимости.

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Применяем миграции.

```
python manage.py migrate
```

5. [Опционально] Загружаем ДЕМО-данные в базу.

```
python manage.py load_csv
```

6. Запускаем проект.

```
python manage.py runserver
```

## Панель администратора

Администратор приложения может добавлять все вручную через панель
администратора Django. Она доступна по адресу:

```
http://<адрес_вашего_проекта>/admin/
```

## Документация

Полная документация API доступна по адресу:

```
http://<адрес_вашего_проекта>/redoc/
```

Примеры работы с этим чудесным API показаны ниже.

### Регистрация пользователя

Адрес запроса:

```
POST http://<адрес_вашего_проекта>/api/v1/auth/signup/
```

Тело запроса:

```
{
    "email": "user@example.com",
    "username": "string"
}
```

Ответ:

```
{
    "email": "user@example.com",
    "username": "string"
}
```

После отправки запроса должно быть получено письмо с confirmation_code, который
в дальнейшем применяется для получения JWT-токенов.

### Получение JWT-токенов

```
POST http://<адрес_вашего_проекта>/api/v1/auth/token/
```

Тело запроса:

```
{
    "username": "string",
    "confirmation_code": "string"
}
```

Ответ:

```
{
    "token": "string"
}
```

### Получение информации о произведении

```
GET http://<адрес_вашего_проекта>/api/v1/titles/{titles_id}/
```

Ответ:

```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
> Другие запросы доступны в полной документации.