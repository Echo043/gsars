# Generated by Django 4.1.2 on 2022-11-19 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GsarsMain', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='email',
            field=models.CharField(max_length=35),
        ),
        migrations.AlterField(
            model_name='students',
            name='password',
            field=models.CharField(default='ChangeYourPassword', max_length=255),
        ),
    ]