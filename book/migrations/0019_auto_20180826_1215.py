# Generated by Django 2.0.7 on 2018-08-26 12:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0018_auto_20180823_0514'),
    ]

    operations = [
        migrations.CreateModel(
            name='DevoteRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DevoteTime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='book',
            name='Devoter',
        ),
        migrations.AddField(
            model_name='devoterecord',
            name='Book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Book'),
        ),
        migrations.AddField(
            model_name='devoterecord',
            name='User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
