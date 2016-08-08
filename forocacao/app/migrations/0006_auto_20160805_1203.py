# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image
from django.conf import settings
import colorfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20160804_1704'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'ordering': ['start', 'name'], 'verbose_name': 'Actividad', 'verbose_name_plural': 'Actividades'},
        ),
        migrations.AlterModelOptions(
            name='attendee',
            options={'ordering': ['first_name', 'last_name'], 'verbose_name': 'Participante', 'verbose_name_plural': 'Participantes'},
        ),
        migrations.AlterModelOptions(
            name='attendeepayment',
            options={'ordering': ['-date'], 'verbose_name': 'Pago del participante', 'verbose_name_plural': 'Pagos del participante'},
        ),
        migrations.AlterModelOptions(
            name='attendeereceipt',
            options={'ordering': ['-date'], 'verbose_name': 'Recibo', 'verbose_name_plural': 'Recibos'},
        ),
        migrations.AlterModelOptions(
            name='attendeetype',
            options={'ordering': ['name'], 'verbose_name': 'Tipo de Participante', 'verbose_name_plural': 'Tipos de Participante'},
        ),
        migrations.AlterModelOptions(
            name='attendeetypeevent',
            options={'verbose_name': 'Tipo de participante en evento', 'verbose_name_plural': 'Tipo de participantes en eventos'},
        ),
        migrations.AlterModelOptions(
            name='content',
            options={'ordering': ['name'], 'verbose_name': 'Contenido', 'verbose_name_plural': 'Contenidos'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['-start'], 'verbose_name': 'Evento', 'verbose_name_plural': 'Eventos'},
        ),
        migrations.AlterModelOptions(
            name='eventbadge',
            options={'ordering': ['field'], 'verbose_name': 'Gafete', 'verbose_name_plural': 'Gafetes'},
        ),
        migrations.AlterModelOptions(
            name='font',
            options={'ordering': ['name'], 'verbose_name': 'Fuente', 'verbose_name_plural': 'Fuentes'},
        ),
        migrations.AlterModelOptions(
            name='invited',
            options={'ordering': ['first_name', 'last_name'], 'verbose_name': 'Invitado', 'verbose_name_plural': 'Invitado'},
        ),
        migrations.AlterModelOptions(
            name='paymentmethod',
            options={'ordering': ['name'], 'verbose_name': 'Forma de pago', 'verbose_name_plural': 'Formas de pago'},
        ),
        migrations.AlterModelOptions(
            name='profession',
            options={'ordering': ['name'], 'verbose_name': 'Profesi\xf3n', 'verbose_name_plural': 'Profesiones'},
        ),
        #migrations.RemoveField(
        #    model_name='organization',
        #    name='email',
        #),
        migrations.AlterField(
            model_name='activity',
            name='end',
            field=models.DateTimeField(null=True, verbose_name='Fin', blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='image_footer',
            field=filer.fields.image.FilerImageField(related_name='activity_footers', verbose_name='Imagen de abajo', blank=True, to='filer.Image', null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='organizer',
            field=models.ForeignKey(verbose_name='Organizador', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='start',
            field=models.DateTimeField(null=True, verbose_name='Inicio', blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='text',
            field=models.TextField(help_text='Try and enter few some more lines', verbose_name='Descripci\xf3n de actividad', blank=True),
        ),
        migrations.AlterField(
            model_name='attendeepayment',
            name='amount',
            field=models.DecimalField(verbose_name='Monto', max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='attendeepayment',
            name='attendee',
            field=models.ForeignKey(related_name='payments', verbose_name='Participante', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='attendeepayment',
            name='date',
            field=models.DateField(verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='attendeepayment',
            name='payment_method',
            field=models.ForeignKey(verbose_name='Forma de pago', to='app.PaymentMethod'),
        ),
        migrations.AlterField(
            model_name='attendeepayment',
            name='reference',
            field=models.CharField(max_length=20, verbose_name='Referencia'),
        ),
        migrations.AlterField(
            model_name='attendeereceipt',
            name='attendee',
            field=models.OneToOneField(related_name='receipt', verbose_name='Participante', to='app.Attendee'),
        ),
        migrations.AlterField(
            model_name='attendeereceipt',
            name='date',
            field=models.DateField(verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='attendeereceipt',
            name='reference',
            field=models.CharField(max_length=20, verbose_name='Referencia'),
        ),
        migrations.AlterField(
            model_name='attendeetypeevent',
            name='attendeetype',
            field=models.ForeignKey(verbose_name='Tipo de Participante', to='app.AttendeeType'),
        ),
        migrations.AlterField(
            model_name='attendeetypeevent',
            name='eb_price',
            field=models.DecimalField(verbose_name='Precio Temprano', max_digits=8, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='attendeetypeevent',
            name='event',
            field=models.ForeignKey(verbose_name='Evento', to='app.Event'),
        ),
        migrations.AlterField(
            model_name='attendeetypeevent',
            name='extra_price',
            field=models.DecimalField(verbose_name='Precio Precongreso', max_digits=8, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='attendeetypeevent',
            name='price',
            field=models.DecimalField(verbose_name='Precio', max_digits=8, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='content',
            name='event',
            field=models.ForeignKey(related_name='contents', verbose_name='Evento', to='app.Event'),
        ),
        migrations.AlterField(
            model_name='content',
            name='title',
            field=models.CharField(max_length=200, verbose_name='T\xedtulo'),
        ),
        migrations.AlterField(
            model_name='content',
            name='title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='T\xedtulo'),
        ),
        migrations.AlterField(
            model_name='content',
            name='title_es',
            field=models.CharField(max_length=200, null=True, verbose_name='T\xedtulo'),
        ),
        migrations.AlterField(
            model_name='event',
            name='activities',
            field=models.ManyToManyField(to='app.Activity', verbose_name='Actividades', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='activities_label',
            field=models.CharField(max_length=50, null=True, verbose_name='Etiqueta de actividades', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='badge_color',
            field=colorfield.fields.ColorField(default='ffffff', max_length=10, verbose_name='Color del gafete'),
        ),
        migrations.AlterField(
            model_name='event',
            name='badge_size_x',
            field=models.IntegerField(null=True, verbose_name='Gafete tama\xf1o X', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='badge_size_y',
            field=models.IntegerField(null=True, verbose_name='Gafete tama\xf1o Y', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='eb_end',
            field=models.DateField(null=True, verbose_name='Fin registro temprano', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='eb_start',
            field=models.DateField(null=True, verbose_name='Inicio registro temprano', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(null=True, verbose_name='Fin', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='image_footer',
            field=filer.fields.image.FilerImageField(related_name='event_footers', verbose_name='Imagen de abajo', blank=True, to='filer.Image', null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Evento'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Evento'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name_es',
            field=models.CharField(max_length=200, null=True, verbose_name='Evento'),
        ),
        migrations.AlterField(
            model_name='event',
            name='organizer',
            field=models.CharField(max_length=200, null=True, verbose_name='Organizador', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='payment_methods',
            field=models.ManyToManyField(to='app.PaymentMethod', verbose_name='Formas de pago', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='pdflogo',
            field=filer.fields.image.FilerImageField(related_name='event_pdflogos', verbose_name='Logo PDF', blank=True, to='filer.Image', null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='place',
            field=models.CharField(max_length=200, null=True, verbose_name='Lugar', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='professions',
            field=models.ManyToManyField(to='app.Profession', verbose_name='Profesiones', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(null=True, verbose_name='Inicio', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.CharField(default='draft', max_length=20, verbose_name='Estado', choices=[('inactive', 'deactivado'), ('draft', 'borrador'), ('published', 'publicado'), ('frontpage', 'portada')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='text',
            field=models.TextField(help_text='Try and enter few some more lines', verbose_name='Descripci\xf3n del evento', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=200, null=True, verbose_name='T\xedtulo', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='T\xedtulo', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='title_es',
            field=models.CharField(max_length=200, null=True, verbose_name='T\xedtulo', blank=True),
        ),
        migrations.AlterField(
            model_name='eventbadge',
            name='event',
            field=models.ForeignKey(verbose_name='Evento', to='app.Event'),
        ),
        migrations.AlterField(
            model_name='eventbadge',
            name='field',
            field=models.CharField(max_length=50, verbose_name='Campo', choices=[('event', 'Evento'), ('name', 'Nombre completo'), ('first_name', 'Nombre'), ('last_name', 'Apellido'), ('profession', 'Profesi\xf3n'), ('country', 'Pa\xeds'), ('type', 'Tipo'), ('email', 'Correo electr\xf3nico'), ('text', 'Texto'), ('logo', 'Logo'), ('photo', 'Foto'), ('organization', 'Organizaci\xf3n')]),
        ),
        migrations.AlterField(
            model_name='eventbadge',
            name='font',
            field=models.ForeignKey(verbose_name='Fuente', blank=True, to='app.Font', null=True),
        ),
        migrations.AlterField(
            model_name='eventbadge',
            name='size',
            field=models.IntegerField(verbose_name='Tama\xf1o'),
        ),
        migrations.AlterField(
            model_name='field',
            name='event',
            field=models.ForeignKey(related_name='fields', verbose_name='Evento', to='app.Event'),
        ),
        migrations.AlterField(
            model_name='font',
            name='filename',
            field=models.CharField(unique=True, max_length=250, verbose_name='Archivo'),
        ),
        migrations.AlterField(
            model_name='invited',
            name='first_name',
            field=models.CharField(max_length=200, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='invited',
            name='last_name',
            field=models.CharField(max_length=200, verbose_name='Apellido'),
        ),
        migrations.AlterField(
            model_name='invited',
            name='organization',
            field=models.CharField(max_length=50, null=True, verbose_name='Organizaci\xf3n', blank=True),
        ),
        migrations.AlterField(
            model_name='logo',
            name='event',
            field=models.ForeignKey(related_name='logos', verbose_name='Evento', to='app.Event'),
        ),
        migrations.AlterField(
            model_name='news',
            name='event',
            field=models.ForeignKey(related_name='news', verbose_name='Evento', to='app.Event'),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=200, verbose_name='T\xedtulo'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='event',
            field=models.ForeignKey(verbose_name='Evento', to='app.Event'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='photo',
            field=models.ImageField(upload_to=b'', null=True, verbose_name='Foto', blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='text',
            field=models.TextField(verbose_name='Descripci\xf3n', blank=True),
        ),
        migrations.AlterField(
            model_name='profession',
            name='text',
            field=models.TextField(help_text='Try and enter few some more lines', verbose_name='Descripci\xf3n de profesi\xf3n', blank=True),
        ),
    ]
