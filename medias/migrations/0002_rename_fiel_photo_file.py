# Generated by Django 4.2.2 on 2023-07-02 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medias', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='fiel',
            new_name='file',
        ),
    ]
