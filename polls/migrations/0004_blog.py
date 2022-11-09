# Generated by Django 4.0.8 on 2022-11-08 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_boxtd_delete_boxtable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('writer', models.CharField(max_length=100)),
                ('pub_date', models.DateTimeField()),
                ('body', models.TextField()),
            ],
        ),
    ]