# Generated by Django 4.1.7 on 2023-03-23 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_alter_article_published_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='published_date',
        ),
    ]
