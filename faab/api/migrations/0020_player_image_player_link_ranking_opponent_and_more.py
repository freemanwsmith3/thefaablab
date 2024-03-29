# Generated by Django 4.1 on 2023-09-21 11:56

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_player_image_player_link_team_abbreviation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='image',
            field=models.CharField(max_length=256, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='player',
            name='link',
            field=models.CharField(max_length=256, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='ranking',
            name='opponent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='opponents', to='api.team'),
        ),
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='api.position'),
        ),
        migrations.AlterField(
            model_name='player',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='api.team'),
        ),
        migrations.AlterField(
            model_name='ranking',
            name='rank',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(200)]),
        ),
        migrations.AlterField(
            model_name='team',
            name='abbreviation',
            field=models.CharField(max_length=4, unique=True),
        ),
    ]
