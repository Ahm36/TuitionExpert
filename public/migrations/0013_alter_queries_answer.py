# Generated by Django 4.0.4 on 2022-07-01 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0012_queries'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queries',
            name='answer',
            field=models.CharField(max_length=90, null=True),
        ),
    ]
