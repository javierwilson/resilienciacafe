# -*- coding: utf-8 -*-
from datetime import date
from PIL import Image, ImageDraw, ImageFont
import textwrap

from django.core.urlresolvers import reverse
from django.template.defaultfilters import date as _date
from django.utils import timezone

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import qr
from reportlab.graphics.barcode import code128
from reportlab.graphics.barcode import code93, code39
from reportlab.graphics.barcode import eanbc
from reportlab.graphics.shapes import Drawing

from .png import get_barcode



def draw(c, string, x, y, color=colors.black, font='Helvetica', size=12):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x, y, string)



def createPDF(participant, where):

    c = canvas.Canvas(where)

    c.pagesize = letter
    c.setTitle("%s : %s" % (participant.event.name, participant.full_name()))
    width, height = letter
    y = hstart = height-20-50
    x = wstart = 80

    #draw(c, "Evento", x, y, size=10, color=colors.grey)
    y -= 20
    draw(c, participant.event.name, x, y, size=22)
    y -= 20

    draw(c, "Fecha y Hora", x, y, size=10, color=colors.grey)
    y -= 20
    draw(c, _date(timezone.localtime(participant.event.start), 'N j, Y, P'), x, y)
    y += 20

    draw(c, "Ubicación", x+200, y, size=10, color=colors.grey)
    y -= 20
    draw(c, participant.event.place, x+200, y)
    y -= 20

    draw(c, "Participante", x, y, size=10, color=colors.grey)
    y -= 20
    draw(c, participant.full_name(), x, y)
    y += 20

    draw(c, "Organización", x+200, y, size=10, color=colors.grey)
    y -= 20
    draw(c, participant.organization, x+200, y)
    y -= 20

    draw(c, u"País", x, y, size=10, color=colors.grey)
    y -= 20
    draw(c, str(participant.country.name), x, y)
    y += 20

    draw(c, "Cargo", x+200, y, size=10, color=colors.grey)
    y -= 20
    draw(c, participant.position, x+200, y)
    y += 20

    #lines = textwrap.fill(participant.event.pdfnote, 60).splitlines()
    lines = (participant.event.pdfnote) % { 'full_name': participant.first_name,}
    lines = lines.splitlines()
    tmp = y
    y -= 100
    for line in lines:
        draw(c, line, x, y)
        y -= 20
    y = tmp

    # insert logo
    #if participant.event.logo:
    #    logo = Image.open(participant.event.logo.file.file)
    #    logo_width = logo.size[0]
    #    logo_height = logo.size[1]
    #    #logo._restrictSize(2 * inch, 1 * inch)
    #    #logo.thumbnail((120,100))
    #    logo = participant.event.logo.file.file.name
    #    c.drawImage(logo, wstart-100, hstart-(logo_height/2), width=logo_width/2, height=logo_height/2)

    # insert header
    if participant.event.pdflogo:
        logo = Image.open(participant.event.pdflogo.file.file)
        logo_width = logo.size[0]
        logo_height = logo.size[1]
        logo = participant.event.pdflogo.file.file.name
        #c.drawImage(logo, wstart, hstart-(logo_height/2), width=logo_width/2, height=logo_height/2)
        c.drawImage(logo, 30, hstart-(logo_height/2)+50, width=612-15-(30*2), preserveAspectRatio=True)
        #c.drawImage(logo, wstart, hstart-(logo_height/2)+50, width=6.5*inch, preserveAspectRatio=True)

    # FIXME do we need to do it the 'contact way' ?
    contact = {
        'name': "%s: %s" % (participant.id, participant.full_name()),
        'phone_number': participant.phone,
        'email': participant.email,
        'url': reverse('app:detail', kwargs={'username': participant.username}),
        'company': participant.organization,
    }

    # draw barcode
    #value = contact['name']
    #barcode128 = code128.Code128(value)
    #barcode128.drawOn(c, wstart-17, y-80)
    #barcode128 = code128.Code128(contact['name'][:20])
    #barcode128.drawOn(c, wstart-17, y-110)

    badge_size_x = 220
    badge_size_y = 150
    short_full_name = "%s: %s" % (participant.id, participant.short_full_name())
    barcode = get_barcode(short_full_name, badge_size_x-4)
    renderPDF.draw(barcode, c, wstart-17, y-80)


    # draw a QR code
    qr_code = qr.QrCodeWidget(contact['name'])
    bounds = qr_code.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    d = Drawing(100, 100, transform=[100./width,0,0,100./height,0,0])
    d.add(qr_code)
    #renderPDF.draw(d, c, wstart+320, y-80)

    c.showPage()
    c.save()
