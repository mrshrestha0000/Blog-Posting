# Generated by Django 4.1.7 on 2023-03-23 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0014_article_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.CharField(blank=True, max_length=22, null=True),
        ),
    ]
