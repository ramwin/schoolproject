# Generated by Django 5.1.3 on 2024-11-26 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0009_lesson_parent_tag_student_age_child'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateTimeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('now', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
