# Generated by Django 4.2 on 2023-05-24 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asker', '0008_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='media/media/Uploads/avatar/1.png', upload_to='Uploads/avatar/'),
        ),
    ]
