# Generated by Django 5.0.2 on 2024-05-06 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_merge_20240507_0733'),
    ]

    operations = [
        migrations.CreateModel(
            name='Klass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('students', models.ManyToManyField(to='school.student')),
            ],
        ),
    ]