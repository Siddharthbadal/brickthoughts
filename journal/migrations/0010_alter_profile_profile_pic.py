# Generated by Django 4.1 on 2022-08-29 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0009_alter_profile_thoughts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to=''),
        ),
    ]