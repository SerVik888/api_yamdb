import csv
from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand
from reviews.models import (
    Genre, Category, Title, GenreTitle, Review, Comment, User
)


class Command(BaseCommand):
    help = 'Import data from CSV files into the database'

    def handle(self, *args, **kwargs):
        with open('static/data/users.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    User.objects.create(
                        id=row['id'],
                        username=row['username'],
                        email=row['email'],
                        role=row['role'],
                        bio=row['bio'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                    )
                except IntegrityError:
                    print(f"Skipping row due to IntegrityError: {row}")
        with open(
            'static/data/category.csv', 'r', encoding='utf-8'
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    Category.objects.create(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug'],
                    )
                except IntegrityError:
                    print(f"Skipping row due to IntegrityError: {row}")

        with open('static/data/genre.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    Genre.objects.create(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug'],
                    )
                except IntegrityError:
                    print(f"Skipping row due to IntegrityError: {row}")

        with open('static/data/titles.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    Title.objects.create(
                        id=row['id'],
                        name=row['name'],
                        year=row['year'],
                        category_id=row['category'],
                    )
                except IntegrityError:
                    print(f"Skipping row due to IntegrityError: {row}")

        with open(
            'static/data/genre_title.csv', 'r', encoding='utf-8'
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    GenreTitle.objects.create(
                        id=row['id'],
                        genre_id=row['genre_id'],
                        title_id=row['title_id'],
                    )
                except IntegrityError:
                    print(f"Skipping row due to IntegrityError: {row}")

        with open('static/data/review.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    Review.objects.create(
                        id=row['id'],
                        text=row['text'],
                        score=row['score'],
                        pub_date=row['pub_date'],
                        author_id=row['author'],
                        title_id=row['title_id'],
                    )
                except IntegrityError:
                    print(f"Skipping row due to IntegrityError: {row}")

        with open(
            'static/data/comments.csv', 'r', encoding='utf-8'
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    Comment.objects.create(
                        id=row['id'],
                        review_id=row['review_id'],
                        text=row['text'],
                        author_id=row['author'],
                        pub_date=row['pub_date'],
                    )
                except IntegrityError:
                    print(f"Skipping row due to IntegrityError: {row}")
