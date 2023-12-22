# Generated by Django 4.2.6 on 2023-12-22 14:22

from django.db import migrations, models
import memento_back.minio_storage


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_like_remove_likemoment_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moment',
            name='image',
            field=models.ImageField(storage=memento_back.minio_storage.MinioStorage, upload_to='moments'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profilephoto',
            field=models.ImageField(blank=True, storage=memento_back.minio_storage.MinioStorage, upload_to='profilephoto'),
        ),
    ]
