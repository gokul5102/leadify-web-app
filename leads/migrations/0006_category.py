# Generated by Django 3.1.5 on 2021-02-15 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0005_auto_20210212_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
    ]
