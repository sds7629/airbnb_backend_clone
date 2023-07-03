# Generated by Django 4.2.2 on 2023-07-03 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_alter_room_category_alter_room_owner'),
        ('experiences', '0003_alter_experience_category_alter_experience_host_and_more'),
        ('medias', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='experiences',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medias', to='experiences.experience'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medias', to='rooms.room'),
        ),
    ]
