# Generated by Django 4.2.14 on 2024-07-17 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forms_app', '0002_resulttablemodel_answer_text_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resulttablemodel',
            name='answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='forms_app.answermodel', verbose_name='Ответ'),
        ),
    ]
