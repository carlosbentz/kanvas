# Generated by Django 3.2.6 on 2021-08-22 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submissions',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='submissions',
            name='users',
        ),
        migrations.DeleteModel(
            name='Activity',
        ),
        migrations.DeleteModel(
            name='Submissions',
        ),
    ]
