# Generated by Django 2.1.3 on 2019-05-12 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_history_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='lunch',
            name='credit',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='roomamenity',
            name='credit',
            field=models.IntegerField(default=0),
        ),
    ]