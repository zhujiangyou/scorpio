# Generated by Django 2.1.3 on 2019-05-22 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_merge_20190520_2033'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeaBreak',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='teaBreak')),
                ('text', models.CharField(default='', max_length=5000)),
            ],
        ),
    ]