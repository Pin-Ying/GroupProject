# Generated by Django 5.1 on 2024-10-16 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_alter_movie_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='screen_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]