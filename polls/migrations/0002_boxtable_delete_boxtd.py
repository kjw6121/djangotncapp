# Generated by Django 4.0.8 on 2022-11-07 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='boxtable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pbox', models.CharField(blank=True, max_length=50, null=True)),
                ('qty', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'boxtd',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='boxtd',
        ),
    ]