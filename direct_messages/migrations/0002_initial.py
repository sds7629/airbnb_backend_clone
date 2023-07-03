# Generated by Django 4.2.2 on 2023-07-03 15:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('direct_messages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='DMS', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chattingroom',
            name='users',
            field=models.ManyToManyField(related_name='ChattingDMS', to=settings.AUTH_USER_MODEL),
        ),
    ]
