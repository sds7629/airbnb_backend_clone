# Generated by Django 4.2.2 on 2023-07-01 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_room_name_alter_amenity_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='amenity',
            options={'verbose_name_plural': 'Amenities'},
        ),
    ]
