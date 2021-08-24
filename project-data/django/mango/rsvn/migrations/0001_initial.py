# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('agency', models.CharField(max_length=30)),
                ('contact', models.CharField(blank=True, max_length=30)),
                ('telephone', models.CharField(blank=True, max_length=20)),
                ('fax', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['agency'],
            },
        ),
        migrations.CreateModel(
            name='AgentRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('agent', models.ForeignKey(to='rsvn.Agent',on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='CurrentLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('date', models.DateField(unique=True)),
                ('log', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128)),
                ('pax', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('descr', models.TextField()),
                ('venue', models.CharField(max_length=90, choices=[('pool', 'Swimming Pool'), ('confroom2', 'Conference 2nd'), ('confroom3', 'Conference 3rd'), ('cafe', 'Cafe'), ('vcourt', 'Volleyball Court'), ('lobby', 'Lobby'), ('back', 'Back Space'), ('other', 'Other')])),
                ('dateStart', models.DateField()),
                ('timeStart', models.TimeField(default='00:00:00')),
                ('dateEnd', models.DateField()),
                ('timeEnd', models.TimeField(default='00:00:00')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('rateName', models.CharField(max_length=512)),
                ('number', models.CharField(max_length=100)),
                ('date_created', models.DateField(auto_now=True)),
                ('date_sent', models.DateField(default=datetime.date(2010, 1, 1))),
                ('date_paid', models.DateField(default=datetime.date(2010, 1, 1))),
                ('text_record', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('clerk', models.CharField(max_length=40)),
                ('time', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(max_length=64)),
                ('desc', models.CharField(max_length=256)),
                ('cost', models.DecimalField(max_digits=12, decimal_places=2)),
                ('units', models.IntegerField(default=1)),
                ('amount', models.DecimalField(max_digits=12, decimal_places=2)),
                ('invoice', models.ForeignKey(to='rsvn.Invoice',on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='RateAtom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('rateName', models.CharField(blank=True, max_length=512)),
                ('rateType', models.CharField(max_length=128, choices=[('standard', 'Standard'), ('deluxe', 'Deluxe'), ('pool_deluxe', 'Pool Deluxe'), ('lanai', 'Lanai'), ('presidential', 'Presidential'), ('manor', 'Manor'), ('SERVICE', 'SERVICE'), ('suites', 'Suites')])),
                ('lowSeason', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12)),
                ('highSeason', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12)),
                ('peakSeason', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='RateHeading',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=256)),
                ('descr', models.CharField(max_length=1028)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('info', models.CharField(blank=True, max_length=512)),
                ('roomstatus', models.CharField(blank=True, max_length=13, choices=[('checkin', 'Check In'), ('checkout', 'Check Out'), ('clean', 'Clean'), ('dirty', 'Dirty'), ('working', 'Working'), ('none', 'None')])),
            ],
        ),
        migrations.CreateModel(
            name='RoomInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('number', models.CharField(max_length=5)),
                ('type', models.CharField(max_length=25, choices=[('standard', 'Standard'), ('deluxe', 'Deluxe'), ('pool_deluxe', 'Pool Deluxe'), ('lanai', 'Lanai'), ('presidential', 'Presidential'), ('manor', 'Manor'), ('suites', 'Suites')])),
                ('beds', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('connect', models.CharField(blank=True, max_length=5)),
                ('notes', models.TextField(blank=True)),
                ('current', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='Rsvn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=13, choices=[('notconfirmed', 'Not Confirmed'), ('confirmed', 'Confirmed'), ('checkin', 'Checking In'), ('checkout', 'Checking Out'), ('notpaid', 'Not Paid'), ('prepaid', 'Prepaid'), ('cancel', 'Cancel'), ('noshow', 'No Show')])),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
                ('source', models.CharField(max_length=20, choices=[('local_fit', 'Local FIT'), ('tour', 'Tour Agency'), ('fit', 'Tour FIT'), ('govt', 'Government'), ('promo', 'Promotional'), ('rack', 'Rack Rate')])),
                ('phone1', models.CharField(max_length=20)),
                ('phone2', models.CharField(blank=True, max_length=20)),
                ('dateIn', models.DateField()),
                ('dateOut', models.DateField()),
                ('rooms', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('type', models.CharField(max_length=15, choices=[('standard', 'Standard'), ('deluxe', 'Deluxe'), ('pool_deluxe', 'Pool Deluxe'), ('lanai', 'Lanai'), ('presidential', 'Presidential'), ('manor', 'Manor'), ('suites', 'Suites')])),
                ('beds', models.IntegerField(default=2, validators=[django.core.validators.MinValueValidator(1)])),
                ('adult', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('child', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('infant', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('notes', models.TextField(blank=True)),
                ('city', models.CharField(blank=True, max_length=30)),
                ('country', models.CharField(max_length=30)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('confirm', models.CharField(blank=True, max_length=20)),
                ('clerk', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='RsvnBlog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('clerk', models.CharField(max_length=40)),
                ('time', models.DateTimeField(auto_now=True)),
                ('desc', models.TextField()),
                ('rsvn', models.ForeignKey(to='rsvn.Rsvn',on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Scheme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('gridColor', models.CharField(default='white', max_length=15, choices=[('White', 'White'), ('Burlywood', 'Burlywood'), ('Red', 'Red'), ('Cyan', 'Cyan'), ('Blue', 'Blue'), ('Green', 'Green'), ('Orange', 'Orange'), ('RoyalBlue', 'RoyalBlue'), ('Orchid', 'Orchid'), ('NavajoWhite', 'NavajoWhite'), ('Maroon', 'Maroon'), ('Sienna', 'Sienna'), ('Yellow', 'Yellow'), ('Purple', 'Purple'), ('DarkKhaki', 'DarkKhaki'), ('Salmon', 'Salmon'), ('SeaGreen', 'SeaGreen'), ('OrangeRed', 'OrangeRed'), ('YellowGreen', 'YellowGreen'), ('DarkCyan', 'DarkCyan'), ('Black', 'Black'), ('HotPink', 'HotPink'), ('Gray', 'Gray'), ('Coral', 'Coral'), ('SaddleBrown', 'SaddleBrown'), ('SlateBlue', 'SlateBlue')])),
                ('rsvnColor', models.CharField(default='white', max_length=15, choices=[('White', 'White'), ('Burlywood', 'Burlywood'), ('Red', 'Red'), ('Cyan', 'Cyan'), ('Blue', 'Blue'), ('Green', 'Green'), ('Orange', 'Orange'), ('RoyalBlue', 'RoyalBlue'), ('Orchid', 'Orchid'), ('NavajoWhite', 'NavajoWhite'), ('Maroon', 'Maroon'), ('Sienna', 'Sienna'), ('Yellow', 'Yellow'), ('Purple', 'Purple'), ('DarkKhaki', 'DarkKhaki'), ('Salmon', 'Salmon'), ('SeaGreen', 'SeaGreen'), ('OrangeRed', 'OrangeRed'), ('YellowGreen', 'YellowGreen'), ('DarkCyan', 'DarkCyan'), ('Black', 'Black'), ('HotPink', 'HotPink'), ('Gray', 'Gray'), ('Coral', 'Coral'), ('SaddleBrown', 'SaddleBrown'), ('SlateBlue', 'SlateBlue')])),
                ('extraColor', models.CharField(default='white', max_length=15, choices=[('White', 'White'), ('Burlywood', 'Burlywood'), ('Red', 'Red'), ('Cyan', 'Cyan'), ('Blue', 'Blue'), ('Green', 'Green'), ('Orange', 'Orange'), ('RoyalBlue', 'RoyalBlue'), ('Orchid', 'Orchid'), ('NavajoWhite', 'NavajoWhite'), ('Maroon', 'Maroon'), ('Sienna', 'Sienna'), ('Yellow', 'Yellow'), ('Purple', 'Purple'), ('DarkKhaki', 'DarkKhaki'), ('Salmon', 'Salmon'), ('SeaGreen', 'SeaGreen'), ('OrangeRed', 'OrangeRed'), ('YellowGreen', 'YellowGreen'), ('DarkCyan', 'DarkCyan'), ('Black', 'Black'), ('HotPink', 'HotPink'), ('Gray', 'Gray'), ('Coral', 'Coral'), ('SaddleBrown', 'SaddleBrown'), ('SlateBlue', 'SlateBlue')])),
                ('rsvn', models.ForeignKey(to='rsvn.Rsvn',on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=140)),
                ('season', models.CharField(max_length=40, choices=[('high', 'High Season'), ('low', 'Low Season'), ('peak', 'Peak Season')])),
                ('beginDate', models.DateField()),
                ('endDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('breakfast', models.BooleanField(default=False)),
                ('lunch', models.BooleanField(default=False)),
                ('dinner', models.BooleanField(default=False)),
                ('from_airport', models.BooleanField(default=False)),
                ('to_airport', models.BooleanField(default=False)),
                ('dailymaid', models.BooleanField(default=False)),
                ('mango', models.BooleanField(default=False)),
                ('extrabed', models.BooleanField(default=False)),
                ('crib', models.BooleanField(default=False)),
                ('connect', models.BooleanField(default=False)),
                ('earlyin', models.BooleanField(default=False)),
                ('lateout', models.BooleanField(default=False)),
                ('event', models.BooleanField(default=False)),
                ('rsvn', models.ForeignKey(to='rsvn.Rsvn',on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='SideEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128)),
                ('pax', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('descr', models.TextField()),
                ('venue', models.CharField(max_length=90, choices=[('pool', 'Swimming Pool'), ('confroom2', 'Conference 2nd'), ('confroom3', 'Conference 3rd'), ('cafe', 'Cafe'), ('vcourt', 'Volleyball Court'), ('lobby', 'Lobby'), ('back', 'Back Space'), ('other', 'Other')])),
                ('dateStart', models.DateField()),
                ('timeStart', models.TimeField(default='00:00:00')),
                ('dateEnd', models.DateField()),
                ('timeEnd', models.TimeField(default='00:00:00')),
            ],
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('arrive_flight', models.CharField(blank=True, max_length=30)),
                ('arrive_time', models.DateTimeField()),
                ('depart_flight', models.CharField(blank=True, max_length=30)),
                ('depart_time', models.DateTimeField()),
                ('promo', models.TextField(blank=True)),
                ('agent', models.ForeignKey(to='rsvn.Agent',on_delete=models.CASCADE)),
                ('rsvn', models.ForeignKey(to='rsvn.Rsvn',on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='WebRsvn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
                ('phone1', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('dateIn', models.DateField()),
                ('dateOut', models.DateField()),
                ('rooms', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('type', models.CharField(max_length=15)),
                ('beds', models.IntegerField(default=2, validators=[django.core.validators.MinValueValidator(1)])),
                ('adult', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('child', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('infant', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('city', models.CharField(blank=True, max_length=30)),
                ('country', models.CharField(max_length=30)),
                ('inquiry', models.CharField(blank=True, max_length=20)),
                ('rsvn', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='roominfo',
            field=models.ForeignKey(to='rsvn.RoomInfo',on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='room',
            name='rsvn',
            field=models.ForeignKey(to='rsvn.Rsvn',on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='rateatom',
            name='rateheading',
            field=models.ForeignKey(to='rsvn.RateHeading',on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='invoice',
            name='rateheading',
            field=models.ForeignKey(to='rsvn.RateHeading',on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='invoice',
            name='rsvn',
            field=models.ForeignKey(to='rsvn.Rsvn',on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='event',
            name='rsvn',
            field=models.ForeignKey(to='rsvn.Rsvn',on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='agentrate',
            name='rateheading',
            field=models.ForeignKey(to='rsvn.RateHeading',on_delete=models.CASCADE),
        ),
    ]
