# Generated by Django 4.1 on 2023-07-28 11:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_bid_week'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(200)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('week', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)])),
                ('user', models.CharField(max_length=50)),
                ('Player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rankings', to='api.player')),
            ],
        ),
    ]