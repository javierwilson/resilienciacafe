# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import model_utils.fields
import colorfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
                ('slug', models.SlugField()),
                ('text', models.TextField(help_text='Try and enter few some more lines', verbose_name='Activity description', blank=True)),
                ('archivo', models.FileField(upload_to='activity', null=True, verbose_name='Archivo', blank=True)),
                ('start', models.DateTimeField(null=True, verbose_name='Start', blank=True)),
                ('end', models.DateTimeField(null=True, verbose_name='End', blank=True)),
            ],
            options={
                'ordering': ['start', 'name'],
                'verbose_name': 'Activity',
                'verbose_name_plural': 'Activities',
            },
        ),
        migrations.CreateModel(
            name='AttendeePayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name='Date')),
                ('amount', models.DecimalField(verbose_name='Amount', max_digits=10, decimal_places=2)),
                ('reference', models.CharField(max_length=20, verbose_name='Reference')),
                ('note', models.CharField(max_length=200, null=True, verbose_name='Nota', blank=True)),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'Attendee Payment',
                'verbose_name_plural': 'Attendee Payments',
            },
        ),
        migrations.CreateModel(
            name='AttendeeReceipt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name='Date')),
                ('reference', models.CharField(max_length=20, verbose_name='Reference')),
                ('note', models.CharField(max_length=200, null=True, verbose_name='Nota', blank=True)),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'Attendee Receipt',
                'verbose_name_plural': 'Attendee Receipts',
            },
        ),
        migrations.CreateModel(
            name='AttendeeType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Attendee Type',
                'verbose_name_plural': 'Attendee Types',
            },
        ),
        migrations.CreateModel(
            name='AttendeeTypeEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(verbose_name='Price', max_digits=8, decimal_places=2)),
                ('eb_price', models.DecimalField(verbose_name='Early Bird Price', max_digits=8, decimal_places=2)),
                ('extra_price', models.DecimalField(verbose_name='Extra Activity Price', max_digits=8, decimal_places=2)),
            ],
            options={
                'verbose_name': 'Attendee Type in Event',
                'verbose_name_plural': 'Attendee Types in Events',
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('page', model_utils.fields.StatusField(default='about', max_length=100, no_check_for_status=True, choices=[('about', 'About'), ('contact', 'Contact'), ('info', 'Main description'), ('footer', 'Footer'), ('services', 'Services'), ('404', 'Not Found'), ('confirmation', 'Confirmation'), ('other', 'Other')])),
                ('text', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Content',
                'verbose_name_plural': 'Contents',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Event')),
                ('title', models.CharField(max_length=200, null=True, verbose_name='Title', blank=True)),
                ('organizer', models.CharField(max_length=200, null=True, verbose_name='Organizer', blank=True)),
                ('slug', models.SlugField()),
                ('status', models.CharField(default='draft', max_length=20, verbose_name='Status', choices=[('inactive', 'inactive'), ('draft', 'draft'), ('published', 'published'), ('frontpage', 'frontpage')])),
                ('activities_label', models.CharField(max_length=50, null=True, verbose_name='Activities label', blank=True)),
                ('text', models.TextField(help_text='Try and enter few some more lines', verbose_name='Event description', blank=True)),
                ('pdfnote', models.TextField(null=True, verbose_name='PDF and Approval Note', blank=True)),
                ('reject_note', models.TextField(null=True, verbose_name='Reject Note', blank=True)),
                ('eb_start', models.DateField(null=True, verbose_name='Early Bird Start', blank=True)),
                ('eb_end', models.DateField(null=True, verbose_name='Early Bird End', blank=True)),
                ('start', models.DateTimeField(null=True, verbose_name='Start', blank=True)),
                ('end', models.DateTimeField(null=True, verbose_name='End', blank=True)),
                ('place', models.CharField(max_length=200, null=True, verbose_name='Place', blank=True)),
                ('badge_size_x', models.IntegerField(null=True, verbose_name='Badge size X', blank=True)),
                ('badge_size_y', models.IntegerField(null=True, verbose_name='Badge size Y', blank=True)),
                ('badge_color', colorfield.fields.ColorField(default='ffffff', max_length=10, verbose_name='Badge color')),
                ('template', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'ordering': ['-start'],
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='EventBadge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.CharField(max_length=50, verbose_name='Field', choices=[('event', 'Event'), ('name', 'Complete name'), ('first_name', 'First name'), ('last_name', 'Last name'), ('profession', 'Profession'), ('country', 'Country'), ('type', 'Tipo'), ('email', 'Correo electr\xf3nico'), ('text', 'Texto'), ('logo', 'Logo'), ('photo', 'Photo'), ('organization', 'Organization')])),
                ('color', colorfield.fields.ColorField(default='', max_length=10, null=True, verbose_name='Color', blank=True)),
                ('size', models.IntegerField(verbose_name='Size')),
                ('x', models.IntegerField(verbose_name='X')),
                ('y', models.IntegerField(verbose_name='Y')),
                ('format', models.CharField(max_length=50, null=True, verbose_name='Extra', blank=True)),
            ],
            options={
                'ordering': ['field'],
                'verbose_name': 'Badge',
                'verbose_name_plural': 'Badges',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', model_utils.fields.StatusField(default='document', max_length=100, no_check_for_status=True, choices=[('document', 'Document'), ('phone', 'Telephone'), ('organization', 'Organization'), ('position', 'Position'), ('profession', 'Profession'), ('country', 'Country')])),
                ('label', models.CharField(max_length=100)),
                ('order', models.IntegerField(null=True)),
            ],
            options={
                'ordering': ['event', 'order'],
            },
        ),
        migrations.CreateModel(
            name='Font',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='Nombre')),
                ('filename', models.CharField(unique=True, max_length=250, verbose_name='Filename')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Font',
                'verbose_name_plural': 'Fonts',
            },
        ),
        migrations.CreateModel(
            name='Invited',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=200, verbose_name='First name')),
                ('last_name', models.CharField(max_length=200, verbose_name='Last name')),
                ('organization', models.CharField(max_length=50, null=True, verbose_name='Organization', blank=True)),
                ('email', models.CharField(unique=True, max_length=100, verbose_name='E-Mail')),
            ],
            options={
                'ordering': ['first_name', 'last_name'],
                'verbose_name': 'Invited',
                'verbose_name_plural': 'Invited',
            },
        ),
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
                ('weight', models.IntegerField()),
                ('url', models.URLField(null=True, blank=True)),
            ],
            options={
                'ordering': ['weight'],
                'verbose_name': 'Logos',
                'verbose_name_plural': 'Logos',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('media', models.CharField(max_length=200, verbose_name='Media')),
                ('url', models.URLField()),
                ('date', models.DateField()),
            ],
            options={
                'ordering': ['-date', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Organization')),
                ('email', models.CharField(max_length=100, verbose_name='E-Mail')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Payment Method',
                'verbose_name_plural': 'Payment Methods',
            },
        ),
        migrations.CreateModel(
            name='Profession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
                ('slug', models.SlugField()),
                ('text', models.TextField(help_text='Try and enter few some more lines', verbose_name='Profession description', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Profession',
                'verbose_name_plural': 'Professions',
            },
        ),
    ]
