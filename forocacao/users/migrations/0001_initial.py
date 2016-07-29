# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
import django_countries.fields
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=50, null=True, verbose_name='Phone', blank=True)),
                ('extra', models.BooleanField(default=False, verbose_name='Extra Activity')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True, verbose_name='Country')),
                ('nationality', django_countries.fields.CountryField(blank=True, max_length=2, null=True, verbose_name='Nationality')),
                ('sponsored', models.BooleanField(default=False, verbose_name='Soponsored')),
                ('document', models.CharField(max_length=50, null=True, verbose_name='Document ID', blank=True)),
                ('organization', models.CharField(max_length=50, null=True, verbose_name='Organization', blank=True)),
                ('position', models.CharField(max_length=50, null=True, verbose_name='Position', blank=True)),
                ('age', models.CharField(blank=True, max_length=1, null=True, choices=[('A', '<=29'), ('B', '30-64'), ('C', '>=65')])),
                ('sex', models.CharField(blank=True, max_length=1, null=True, choices=[('M', 'Male'), ('F', 'Female')])),
                ('address', models.CharField(max_length=200, null=True, verbose_name='Address', blank=True)),
                ('approved', models.BooleanField(default=False, verbose_name='Approved')),
                ('rejected', models.BooleanField(default=False, verbose_name='Rejected')),
                ('photo', models.ImageField(upload_to=b'', null=True, verbose_name='Photo', blank=True)),
                ('text', models.TextField(help_text='Try and enter few some more lines', verbose_name='Biography', blank=True)),
                ('activities', models.ManyToManyField(to='app.Activity', verbose_name='Activity', blank=True)),
                ('event', models.ForeignKey(verbose_name='Event', to='app.Event', null=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('profession', models.ForeignKey(verbose_name='Profession', blank=True, to='app.Profession', null=True)),
                ('responsible', models.ForeignKey(verbose_name='Organization responsible', to='app.Organization', null=True)),
                ('sponsor', models.ForeignKey(verbose_name='Sponsor', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('type', models.ForeignKey(verbose_name='Type', to='app.AttendeeType', null=True)),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Attendee',
                'verbose_name_plural': 'Attendees',
                'permissions': (('can_print_badge', 'Can print badge'), ('can_approve_participant', 'Can approve participant')),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
