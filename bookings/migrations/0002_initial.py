# Generated by Django 4.2.2 on 2023-07-03 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bookings', '0001_initial'),
        ('experiences', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='experience',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to='experiences.experience'),
        ),
    ]
