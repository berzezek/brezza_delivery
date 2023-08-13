# Generated by Django 4.2.4 on 2023-08-12 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0006_alter_deliveryschedule_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='day_of_week',
            field=models.CharField(choices=[('0', 'Понедельник'), ('1', 'Вторник'), ('2', 'Среда'), ('3', 'Четверг'), ('4', 'Пятница'), ('5', 'Суббота'), ('6', 'Воскресенье')], max_length=1),
        ),
    ]