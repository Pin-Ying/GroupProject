# Generated by Django 5.1.2 on 2024-11-04 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataCrawl', '0002_showtimeinfo_full_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='img_src',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='trailer_link',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
