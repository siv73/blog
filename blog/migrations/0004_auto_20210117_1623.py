# Generated by Django 3.1.2 on 2021-01-17 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210117_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=264, unique_for_date='publish'),
        ),
    ]