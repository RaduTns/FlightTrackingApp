# Generated by Django 4.0.5 on 2022-07-17 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DB_work', '0002_alter_flight_altitude_alter_flight_callsign_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='destination',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='flight',
            name='origin',
            field=models.CharField(max_length=100, null=True),
        ),
    ]