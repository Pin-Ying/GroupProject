# Generated by Django 5.1.1 on 2024-09-27 02:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='joining_on',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='movie',
            old_name='area',
            new_name='time',
        ),
        migrations.RenameField(
            model_name='movie',
            old_name='update_time',
            new_name='update_date',
        ),
    ]