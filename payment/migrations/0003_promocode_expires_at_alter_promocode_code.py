# Generated by Django 5.1.7 on 2025-06-05 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_promocode_payment_promocode'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocode',
            name='expires_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='code',
            field=models.CharField(db_index=True, max_length=128, unique=True),
        ),
    ]
