# Generated by Django 3.2.2 on 2021-05-12 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_match'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('data', models.JSONField()),
            ],
        ),
    ]