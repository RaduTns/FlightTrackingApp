# Generated by Django 4.0.5 on 2022-06-26 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('callsign', models.CharField(max_length=100)),
                ('longitude', models.CharField(max_length=100)),
                ('latitude', models.CharField(max_length=100)),
                ('altitude', models.CharField(max_length=100)),
                ('on_ground', models.CharField(max_length=100)),
            ],
        ),
    ]
