# Generated by Django 4.2.5 on 2023-10-17 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_course_price_lesson_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Статус оплаты'),
        ),
    ]
