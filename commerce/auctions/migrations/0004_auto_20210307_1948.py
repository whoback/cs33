# Generated by Django 3.1.7 on 2021-03-07 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_listing_current_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='date_listed',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
