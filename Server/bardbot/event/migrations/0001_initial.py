# Generated by Django 3.2.11 on 2022-01-31 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_uri', models.CharField(max_length=128)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('log', models.TextField()),
            ],
        ),
    ]
