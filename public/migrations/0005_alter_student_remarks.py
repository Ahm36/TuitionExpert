# Generated by Django 4.0.4 on 2022-06-27 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0004_rename_login_logint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='remarks',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]