# Generated by Django 5.0.3 on 2024-03-29 04:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_course_user_courses'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]