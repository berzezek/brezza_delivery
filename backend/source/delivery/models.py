from django.db import models
from django.utils import timezone


class Customer(models.Model):

    title = models.CharField(verbose_name='Наименование', max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Заказчика'
        verbose_name_plural = 'Заказчики'

    def __str__(self):
        return self.title


class TgService(models.Model):

    customer = models.ForeignKey(
        Customer, verbose_name='Заказчик', on_delete=models.DO_NOTHING)
    tg_id = models.CharField(verbose_name='Телеграм ID', max_length=32)
    is_active = models.BooleanField(verbose_name='Активный', default=False)
    name = models.CharField(verbose_name='Имя пользователя',
                            max_length=32, blank=True, null=True)
    description = models.TextField(
        verbose_name='Описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Телеграм ID'
        verbose_name_plural = 'Телеграм ID'

    def __str__(self):
        return f'Telegram {self.customer.title} / {self.name}'


class Order(models.Model):

    customer = models.ForeignKey(
        Customer, verbose_name='Заказчик', on_delete=models.DO_NOTHING)
    dead_line = models.DateTimeField(
        verbose_name='Срок', blank=True, null=True)
    delivered_time = models.DateTimeField(
        'Доставлено в', null=True, blank=True)
    overdue_time = models.DurationField(
        'Просроченное время', blank=True, null=True)
    receiver_name = models.CharField(
        verbose_name='Имя получателя', max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.delivered_time and not self.overdue_time and self.delivered_time > self.dead_line:
            self.overdue_time = self.delivered_time - self.dead_line
        super(Order, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Заказ для доставки'
        verbose_name_plural = 'Заказы для доставки'
        ordering = ['-dead_line']

    def __str__(self):
        local_deadline = timezone.localtime(self.dead_line)
        local_deadline_weekday = local_deadline.strftime('%A')
        return f'{self.customer.title} / {local_deadline_weekday}-{local_deadline.strftime("%H:%M")}'


class Schedule(models.Model):
    DAY_OF_WEEK_CHOICE = [
        ('0', 'Понедельник'),
        ('1', 'Вторник'),
        ('2', 'Среда'),
        ('3', 'Четверг'),
        ('4', 'Пятница'),
        ('5', 'Суббота'),
        ('6', 'Воскресенье'),
    ]

    day_of_week = models.CharField(max_length=1, choices=DAY_OF_WEEK_CHOICE)
    schedule_time = models.TimeField()

    def get_day_of_week_display(self):
        return self.DAY_OF_WEEK_CHOICE[int(self.day_of_week)][1]

    def convert_to_hour_minute(self):
        return self.schedule_time.strftime('%H:%M')

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'
        ordering = ['day_of_week', 'schedule_time']

    def __str__(self):
        return f'{self.get_day_of_week_display()} {self.convert_to_hour_minute()}'


class DeliverySchedule(models.Model):

    customer = models.ForeignKey(
        Customer, verbose_name='Заказчик', on_delete=models.DO_NOTHING)
    delivery_schedule = models.ManyToManyField(
        Schedule,  verbose_name='Расписание')

    def get_schedule_list_to_str(self):
        # Группировка по дням недели
        grouped = {}
        for schedule in self.delivery_schedule.all():
            day = schedule.get_day_of_week_display().lower()
            time = schedule.convert_to_hour_minute()
            if day not in grouped:
                grouped[day] = []
            grouped[day].append(time)

        # Форматирование для вывода
        result_list = []
        for day, times in grouped.items():
            result_list.append(f"{day}: {' * '.join(times)}")

        return ', '.join(result_list)

    class Meta:
        verbose_name = 'Расписание заказа'
        verbose_name_plural = 'Расписание заказов'
        ordering = ['customer']

    def __str__(self):
        return f'{self.customer.title} - {self.get_schedule_list_to_str()}'
