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

### Для подключения к SSH

```bash
ssh root@92.63.177.224
```

password: mxiPKk1T


### Развертываем Docker

```bash
docker-compose up -d --build
```