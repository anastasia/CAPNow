# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-02-09 23:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firmament', '0005_auto_20170201_2201'),
    ]

    operations = [
        migrations.CreateModel(
            name='Judge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='proof',
            name='html',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='proof',
            name='xml',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
