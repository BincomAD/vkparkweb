# Generated by Django 4.2 on 2023-06-10 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asker', '0013_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='Uploads/avatar/1.png', upload_to='Uploads/avatar/'),
        ),
    ]
