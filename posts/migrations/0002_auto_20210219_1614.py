# Generated by Django 2.2 on 2021-02-19 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postfile',
            name='file',
            field=models.FileField(upload_to='postFiles/'),
        ),
    ]