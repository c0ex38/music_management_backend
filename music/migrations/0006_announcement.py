# Generated by Django 5.1.1 on 2024-10-07 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_playlist_store_name_alter_playlist_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('store_name', models.CharField(max_length=100)),
                ('frequency', models.PositiveIntegerField(default=3)),
            ],
        ),
    ]
