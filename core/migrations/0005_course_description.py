# Generated by Django 5.1.7 on 2025-03-26 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_course_price_level_price_levelpurchase_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
    ]
