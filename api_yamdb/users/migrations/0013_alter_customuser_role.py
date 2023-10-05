# Generated by Django 3.2 on 2023-10-05 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20231005_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('user', 'пользователь'), ('moderator', 'модератор'), ('admin', 'администратор')], default='user', max_length=13, verbose_name='Роль'),
        ),
    ]
