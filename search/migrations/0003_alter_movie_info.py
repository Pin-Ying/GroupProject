# Generated by Django 5.1 on 2024-10-16 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_alter_showtimeinfo_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='info',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]