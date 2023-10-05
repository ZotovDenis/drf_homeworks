# Generated by Django 4.2.5 on 2023-10-05 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_payments'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payments',
            options={'verbose_name': 'Платеж', 'verbose_name_plural': 'Платежи'},
        ),
        migrations.AlterField(
            model_name='payments',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('наличные', 'Наличные'), ('перевод на счет', 'Перевод на счет')], max_length=30, null=True, verbose_name='Способ оплаты'),
        ),
    ]
