# Generated by Django 4.1 on 2022-09-05 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_bid_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='position',
            field=models.CharField(default='Runningback', max_length=50),
            preserve_default=False,
        ),
    ]
