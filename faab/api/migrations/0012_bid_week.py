# Generated by Django 4.1 on 2022-09-04 17:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_bid_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='week',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(17)]),
            preserve_default=False,
        ),
    ]