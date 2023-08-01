import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import (
    Category, Comment, Genre, GenreTitle, Review, Title, User
)

CSV_FILES = [
    ('users.csv', User),
    ('category.csv', Category),
    ('genre.csv', Genre),
    ('titles.csv', Title),
    ('genre_title.csv', GenreTitle),
    ('review.csv', Review),
    ('comments.csv', Comment),
]

HEADER_REPLACER = {
    'category': 'category_id',
    'author': 'author_id',
}


class Command(BaseCommand):
    help = 'Загрузка CSV файлов в базу данных'

    def handle(self, *args, **options):

        self.stdout.write(self.style.NOTICE('Идет подготовка...'))

        for _, model in reversed(CSV_FILES):
            model.objects.all().delete()

        self.stdout.write(self.style.NOTICE('Загружаю данные...'))

        for filename, model in CSV_FILES:
            with open(settings.CSV_PATH + filename, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for index, column_name in enumerate(reader.fieldnames):
                    if column_name in HEADER_REPLACER:
                        reader.fieldnames[index] = HEADER_REPLACER[column_name]
                model.objects.bulk_create(
                    model(**row) for row in reader
                )

        self.stdout.write(self.style.SUCCESS('Успешная загрузка!'))
