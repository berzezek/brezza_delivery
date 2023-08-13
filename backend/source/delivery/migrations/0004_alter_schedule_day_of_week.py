# Generated by Django 4.2.4 on 2023-08-12 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0003_schedule_alter_order_options_deliveryschedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='day_of_week',
            field=models.CharField(choices=[(1, 'Понедельник'), (2, 'Вторник'), (3, 'Среда'), (4, 'Четверг'), (5, 'Пятница'), (6, 'Суббота'), (7, 'Воскресенье')], max_length=1),
        ),
    ]