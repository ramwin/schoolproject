# Generated by Django 5.0 on 2024-05-05 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_exam'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='update_datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]