# Generated by Django 5.1 on 2024-10-16 13:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='movie',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('img_src', models.CharField(blank=True, max_length=100, null=True)),
                ('trailer_link', models.CharField(blank=True, max_length=100, null=True)),
                ('movie_type', models.CharField(blank=True, max_length=100, null=True)),
                ('main_actor', models.CharField(blank=True, max_length=100, null=True)),
                ('info', models.CharField(blank=True, max_length=500, null=True)),
                ('release_date', models.DateField(blank=True, max_length=100, null=True)),
                ('running_time', models.CharField(blank=True, max_length=100, null=True)),
                ('screen_type', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='theater',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('cinema', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='showTimeInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(blank=True, max_length=100, null=True)),
                ('time', models.CharField(blank=True, max_length=100, null=True)),
                ('site', models.CharField(blank=True, max_length=100, null=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.movie')),
                ('theater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.theater')),
            ],
        ),
    ]
