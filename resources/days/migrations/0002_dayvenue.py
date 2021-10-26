# Generated by Django 3.2.8 on 2021-10-26 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0002_alter_venue_yelp_id'),
        ('days', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayVenue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pos', models.IntegerField()),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='days.day')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venues.venue')),
            ],
        ),
    ]
