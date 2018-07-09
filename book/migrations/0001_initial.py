# Generated by Django 2.0.6 on 2018-07-08 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ISBN', models.CharField(max_length=30)),
                ('IsBorrowed', models.BooleanField()),
                ('BookName', models.CharField(max_length=250)),
                ('Author', models.CharField(max_length=100)),
                ('Publisher', models.CharField(max_length=100)),
                ('DevoterName', models.CharField(max_length=100)),
            ],
        ),
    ]
