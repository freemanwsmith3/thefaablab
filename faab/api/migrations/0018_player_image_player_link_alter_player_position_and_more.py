# Generated by Django 4.1 on 2023-07-28 12:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_player_image_player_link_alter_player_position_and_more'),
    ]

    operations = [
        
        migrations.AlterField(
            model_name='ranking',
            name='rank',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50)]),
        ),
    ]