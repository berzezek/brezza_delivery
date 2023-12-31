# Brezza Delivery 🚚

## Функциональность

- **Создание записей о заказах**: Сервис автоматически создает запись в базе данных о заказах, которые ожидаются в течение ближайшего часа и 10 минут.
- **Получение информации о доставке**: Заказчики могут зайти в бота и запросить информацию о ближайшей доставке, введя название заведения. В базе идет поиск последней записи о доставке в данном заведении c delivery_time = None. Если такая запись найдена, то бот возвращает информацию о доставке, иначе - сообщение о том, что доставка не найдена.
- **Подтверждение получения заказа**: Если есть ближайшая доставка, заказчик может нажать на кнопку "Получить доставку". При этом в базе данных создается запись с информацией о времени получения и именем получателя. Имя получателя автоматически берется из имени пользователя Telegram.

### Описание проекта

Проект представляет собой сервис на базе фреймворка Django, который взаимодействует с Telegram-ботом @brezza_delivery_bot. Сервис предназначен для обработки заказов и уведомлений о предстоящей доставке в различных заведениях. Заказчики могут взаимодействовать с ботом, чтобы узнать информацию о ближайшей доставке, а также подтвердить получение заказа.

Функциональность
Создание записей о заказах: Сервис автоматически создает запись в базе данных о заказах, которые ожидаются в течение ближайшего часа и 10 минут.

Получение информации о доставке: Заказчики могут зайти в бота и запросить информацию о ближайшей доставке, введя название заведения.

Подтверждение получения заказа: Если есть ближайшая доставка, заказчик может нажать на кнопку "Получить доставку". При этом в базе данных создается запись с информацией о времени получения и именем получателя. Имя получателя автоматически берется из имени пользователя Telegram.

Настройка проекта
Клонирование репозитория: Склонируйте репозиторий на ваш локальный компьютер с помощью команды git clone [<URL репозитория>](https://github.com/berzezek/brezza_delivery.git).

после этого нужно будет создать файл .env в папке backend и заполнить его следующим образом:

```bash
TELEGRAM_BOT_TOKEN=<token>
ADMIN_USERS=(<telegram_id>, <telegram_id>)
HOST_URL=http://web:8000
```

Проект может быть запущет в Docker

```bash
docker-compose up -d --build
```

После этого проект будет доступен по адресу http://localhost

Также можно запустить проект локально

- Сервер

```bash
python3 manage.py runserver
```

- Worker

```bash
celery -A core worker --beat --scheduler django --loglevel=info
```

- Бот

```bash
python3 bot.py
```

Обратная связь
Если у вас возникли вопросы или предложения по улучшению проекта, не стесняйтесь обращаться.
