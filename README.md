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
<img width="468" height="189" alt="image" src="https://github.com/user-attachments/assets/80537936-c3fa-47ea-85ee-aad61bad1038" />

## О проекте

Реализован с использованием fastapi, sqlalchemy и alembic.
