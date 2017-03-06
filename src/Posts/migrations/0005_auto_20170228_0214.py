# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-28 02:14
from __future__ import unicode_literals

import Posts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0004_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='height_Field',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='width_Field',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, height_field=models.IntegerField(default=0), null=True, upload_to=Posts.models.uploadLoc, width_field=models.IntegerField(default=0)),
        ),
    ]