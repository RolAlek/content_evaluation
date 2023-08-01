# Generated by Django 3.2 on 2023-07-30 00:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20230731_0151'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(db_index=True, max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Имя пользователя содержит недопустимый символ', regex='^[\\w.@+-]+$')], verbose_name='Имя пользователя'),
        ),
    ]
