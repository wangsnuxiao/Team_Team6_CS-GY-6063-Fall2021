# Generated by Django 3.2.8 on 2021-10-29 22:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('venues', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DayVenue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pos', models.IntegerField()),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='days.day')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venues.venue')),
            ],
            options={
                'ordering': ['pos'],
            },
        ),
    ]
