# Generated by Django 5.1.7 on 2025-04-29 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_alter_quizquestion_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='is_correct',
            field=models.BooleanField(default=False, verbose_name='Is Correct'),
        ),
    ]
