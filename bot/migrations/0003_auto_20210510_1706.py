# Generated by Django 3.2.2 on 2021-05-10 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_auto_20210510_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='botuser',
            name='username',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='botuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='botuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
