# Generated by Django 5.0.6 on 2024-07-10 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='Recipe_img',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
