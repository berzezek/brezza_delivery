# Brezza Delivery 🚚

## Установка

1. Установить зависимости 🔧

```bash
pip install -r requirements.txt
```

2. Создать базу данных 🗃️

```bash
python manage.py migrate
```

3. Создать суперпользователя 🔐

```bash
python manage.py createsuperuser
```

4. Запустить сервер 🌐

```bash
python manage.py runserver
```

5. Запустить Worker 🛠️

```bash
celery -A core worker --beat --scheduler django --loglevel=info
```

6. Запустить Telegram Bot 🤖

```bash
python manage.py bot
```
