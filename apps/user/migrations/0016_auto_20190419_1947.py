# Generated by Django 2.1.7 on 2019-04-19 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_auto_20190419_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='pid',
            field=models.IntegerField(default=0, verbose_name='父级评论id'),
        ),
    ]
