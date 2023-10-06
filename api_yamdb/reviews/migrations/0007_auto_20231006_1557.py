# Generated by Django 3.2 on 2023-10-06 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_auto_20231005_1810'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ('name',), 'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'default_related_name': 'titles', 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
    ]