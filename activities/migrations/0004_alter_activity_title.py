# Generated by Django 3.2.6 on 2021-08-22 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_activity_submissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]