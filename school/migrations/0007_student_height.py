# Generated by Django 5.0.6 on 2024-06-08 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0006_student_code_student_code_unique'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='height',
            field=models.IntegerField(null=True),
        ),
    ]
