# Generated by Django 5.1.1 on 2024-10-07 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0008_store_remove_announcement_store_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcement',
            name='message',
        ),
        migrations.RemoveField(
            model_name='announcement',
            name='stores',
        ),
        migrations.AddField(
            model_name='announcement',
            name='store_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
