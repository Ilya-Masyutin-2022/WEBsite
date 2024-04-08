# Generated by Django 5.0.2 on 2024-04-08 10:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0008_frontman_bands_frontman'),
    ]

    operations = [
        migrations.AddField(
            model_name='frontman',
            name='m_count',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='bands',
            name='frontman',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='band', to='bands.frontman'),
        ),
    ]
