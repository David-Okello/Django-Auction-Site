# Generated by Django 4.2.7 on 2024-01-10 15:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_watchlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='HighestBidder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('highest_bidder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='highest_bidder', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='highest_bidder', to='auctions.item')),
            ],
        ),
    ]
