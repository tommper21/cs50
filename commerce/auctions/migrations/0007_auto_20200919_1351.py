# Generated by Django 3.1.1 on 2020-09-19 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_category', to='auctions.category'),
        ),
    ]
