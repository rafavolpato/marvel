# Generated by Django 3.2.18 on 2023-02-15 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("character", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="character",
            name="character_id",
            field=models.IntegerField(unique=True),
        ),
    ]
