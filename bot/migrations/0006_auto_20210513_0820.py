# Generated by Django 3.2.2 on 2021-05-13 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_log'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='botuser',
            name='is_open_for_requests',
        ),
        migrations.AddField(
            model_name='botuser',
            name='open_for_requests_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
