# Generated by Django 4.1.7 on 2023-03-23 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0009_remove_article_published_date_article_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
