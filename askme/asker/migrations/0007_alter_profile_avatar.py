# Generated by Django 4.2 on 2023-05-24 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asker', '0006_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(upload_to='static/Uploads/avatar/'),
        ),
    ]
