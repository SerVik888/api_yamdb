# Generated by Django 3.2 on 2023-10-09 09:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+\\Z|me', 'Вы не можете зарегестрировать пользователя с таким именем.')], verbose_name='Ник-нейм пользователя'),
        ),
    ]
