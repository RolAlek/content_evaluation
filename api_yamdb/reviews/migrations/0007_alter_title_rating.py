# Generated by Django 3.2 on 2023-07-29 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_alter_title_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='rating',
            field=models.IntegerField(null=True, verbose_name='Оценка произведения'),
        ),
    ]