# Generated by Django 4.0.8 on 2022-11-17 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_alter_boxtr_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boxtr',
            name='arrival',
            field=models.CharField(blank=True, choices=[(1, '07:30'), (2, '08:00'), (3, '08:30'), (4, '09:00'), (5, '09:30'), (6, '10:00'), (7, '10:30'), (8, '11:00'), (9, '11:30'), (10, '12:00'), (11, '12:30'), (12, '13:00'), (13, '13:30'), (14, '14:00'), (15, '14:30'), (16, '15:00'), (17, '15:30'), (18, '16:00'), (19, '16:30'), (20, '17:00'), (21, '17:30'), (22, '18:00'), (23, '18:30'), (24, '19:00')], max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='boxtr',
            name='box1',
            field=models.CharField(blank=True, choices=[(14, 'DN8 TILT'), (13, 'YF TILT'), (4, 'Height'), (6, 'LX2_10'), (7, 'LX2_12'), (5, 'JOEM'), (8, 'P/W내장'), (9, '파워일반'), (10, '파워포장'), (11, 'PU'), (12, 'XMA'), (1, '일반히터'), (2, 'GPB'), (3, 'GPG'), (15, '기타')], default='', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='boxtr',
            name='box1_qty',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25)], default='0', null=True),
        ),
        migrations.AlterField(
            model_name='boxtr',
            name='box2',
            field=models.CharField(blank=True, choices=[(14, 'DN8 TILT'), (13, 'YF TILT'), (4, 'Height'), (6, 'LX2_10'), (7, 'LX2_12'), (5, 'JOEM'), (8, 'P/W내장'), (9, '파워일반'), (10, '파워포장'), (11, 'PU'), (12, 'XMA'), (1, '일반히터'), (2, 'GPB'), (3, 'GPG'), (15, '기타')], default='', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='boxtr',
            name='box2_qty',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25)], default='0', null=True),
        ),
        migrations.AlterField(
            model_name='boxtr',
            name='box3',
            field=models.CharField(blank=True, choices=[(14, 'DN8 TILT'), (13, 'YF TILT'), (4, 'Height'), (6, 'LX2_10'), (7, 'LX2_12'), (5, 'JOEM'), (8, 'P/W내장'), (9, '파워일반'), (10, '파워포장'), (11, 'PU'), (12, 'XMA'), (1, '일반히터'), (2, 'GPB'), (3, 'GPG'), (15, '기타')], default='', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='boxtr',
            name='box3_qty',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25)], default='0', null=True),
        ),
        migrations.AlterField(
            model_name='boxtr',
            name='box4',
            field=models.CharField(blank=True, choices=[(14, 'DN8 TILT'), (13, 'YF TILT'), (4, 'Height'), (6, 'LX2_10'), (7, 'LX2_12'), (5, 'JOEM'), (8, 'P/W내장'), (9, '파워일반'), (10, '파워포장'), (11, 'PU'), (12, 'XMA'), (1, '일반히터'), (2, 'GPB'), (3, 'GPG'), (15, '기타')], default='', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='boxtr',
            name='box4_qty',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25)], default='0', null=True),
        ),
        migrations.AlterField(
            model_name='boxtr',
            name='box5',
            field=models.CharField(blank=True, choices=[(14, 'DN8 TILT'), (13, 'YF TILT'), (4, 'Height'), (6, 'LX2_10'), (7, 'LX2_12'), (5, 'JOEM'), (8, 'P/W내장'), (9, '파워일반'), (10, '파워포장'), (11, 'PU'), (12, 'XMA'), (1, '일반히터'), (2, 'GPB'), (3, 'GPG'), (15, '기타')], default='', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='boxtr',
            name='box5_qty',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25)], default='0', null=True),
        ),
        migrations.AlterField(
            model_name='boxtr',
            name='flift',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='boxtr',
            name='status',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='boxtr',
            name='truck',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterModelTable(
            name='boxtr',
            table=None,
        ),
    ]
