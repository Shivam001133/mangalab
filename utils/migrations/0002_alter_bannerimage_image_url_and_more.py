# Generated by Django 5.0.9 on 2024-11-07 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerimage',
            name='image_url',
            field=models.URLField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bannerimage',
            name='source_type',
            field=models.CharField(choices=[('image', 'Image'), ('video', 'video')], default='image', max_length=10),
        ),
    ]