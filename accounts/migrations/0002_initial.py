# Generated by Django 5.1.7 on 2025-03-22 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('task_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='interest_categories',
            field=models.ManyToManyField(related_name='interested_users', through='task_manager.UserInterestCategory', to='task_manager.category'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
