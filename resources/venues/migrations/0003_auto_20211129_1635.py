# Generated by Django 3.2.7 on 2021-11-29 21:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('venues', '0002_alter_venue_yelp_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteVenue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.TimeField(auto_now_add=True, verbose_name='Created at')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venues.venue')),
            ],
        ),
        migrations.AddConstraint(
            model_name='favoritevenue',
            constraint=models.UniqueConstraint(fields=('user', 'venue'), name='favoritevenue_unique_user_venue'),
        ),
    ]
