# Generated by Django 4.1.7 on 2023-03-23 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_article_published_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='published_date',
            field=models.DateField(),
        ),
    ]
