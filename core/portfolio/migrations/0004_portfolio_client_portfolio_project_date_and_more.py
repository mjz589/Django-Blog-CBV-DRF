# Generated by Django 4.2.4 on 2023-10-03 22:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0003_alter_portfoliocategory_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="portfolio",
            name="client",
            field=models.CharField(default="myself", max_length=255),
        ),
        migrations.AddField(
            model_name="portfolio",
            name="project_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 10, 4, 2, 20, 47, 20541)
            ),
        ),
        migrations.AddField(
            model_name="portfolio",
            name="project_url",
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
