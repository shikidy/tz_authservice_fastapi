# 🔒 Auth service
Выполнено в рамках технического задания

## 🚀 Deploy

### 📦 Docker

1. Клонируем репозиторий

    ```git clone https://github.com/shikidy/tz_authservice_fastapi```

2. Генерируем ключи для access и refresh токенов, после чего вставляем в .env.

3. Поднимаем doker-compose

    ```docker-compose up```

4. Получаем приложение на 8000 порту. Осталось настроить ngix для проксирования.

## 🔍 Tests

1. Клонируем репозиторий

    ```git clone https://github.com/shikidy/tz_authservice_fastapi```

2. Генерируем ключи для access и refresh токенов, после чего вставляем в .env.

3. Изменяем ENVIRONMENT на local, чтобы автоматически был добавлен тестовый пользователь.

4. Запускаем тесты 

    ```uv run pytest```

## О проекте

Реализован с использованием fastapi, sqlalchemy и alembic.
