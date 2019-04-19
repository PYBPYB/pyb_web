# Generated by Django 2.1.7 on 2019-04-18 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20190416_2123'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('image', models.ImageField(upload_to='', verbose_name='用户上传的图片')),
            ],
            options={
                'verbose_name': '图片',
                'verbose_name_plural': '图片',
            },
        ),
    ]
