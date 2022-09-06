# Generated by Django 4.1 on 2022-09-04 13:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_player_guestcansee_player_week'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='guestCanSee',
        ),
        migrations.RemoveField(
            model_name='player',
            name='mean_value',
        ),
        migrations.RemoveField(
            model_name='player',
            name='week',
        ),
        migrations.AlterField(
            model_name='bid',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='api.player'),
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mean_value', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)])),
                ('week', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(17)])),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='targets', to='api.player')),
            ],
        ),
    ]
