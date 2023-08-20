# Brezza Delivery 🚚

## Установка

### Для локальной разработки

#### Worker

```bash
celery -A core worker --beat --scheduler django --loglevel=info
```

#### Telegram Bot

```bash
python3 bot.py
```
951771677