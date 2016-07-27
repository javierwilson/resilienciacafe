# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import textwrap

from unidecode import unidecode
from reportlab.graphics import renderPM
from reportlab.graphics.barcode import code128
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.barcode import createBarcodeImageInMemory
from reportlab.graphics.shapes import Drawing


def get_barcode(value, width, humanReadable = True):

    #value = value.encode('ascii', 'ignore')
    value = unidecode(value)
    barcode = createBarcodeDrawing('Code128', value = value, humanReadable = humanReadable, fontSize = 8)

    drawing_width = width
    barcode_scale = drawing_width / barcode.width
    drawing_height = barcode.height * barcode_scale

    drawing = Drawing(drawing_width, drawing_height)
    drawing.scale(barcode_scale, barcode_scale)
    drawing.add(barcode, name='barcode')

    return drawing


def createPNG(participant, where):

    event = participant.event

    badge_size_x = event.badge_size_x or 390
    badge_size_y = event.badge_size_y or 260
    badge_color = event.badge_color or "#FFFFFF"

    img = Image.new('RGBA', (badge_size_x, badge_size_y), badge_color)
    draw = ImageDraw.Draw(img)
    draw.rectangle(((0,0),(badge_size_x-1, badge_size_y-1)), outline = "black")

    match = {
            'event': event.name,
            #'name': "%s %s" % (participant.first_name, participant.last_name ),
            'name': "%s %s" % (participant.first_name.partition(' ')[0], participant.last_name.partition(' ')[0]),
            'first_name': participant.first_name,
            'last_name': participant.last_name,
            'profession': participant.profession,
            'organization': participant.organization,
            'country': participant.country.name,
            'type': participant.type,
            'email': participant.email,
        }
    for field in event.eventbadge_set.all():
        x = field.x
        y = field.y
        size = field.size
        if field.field == 'logo':
            if participant.event.logo:
                logo = Image.open(participant.event.logo.file.file)
                logo.thumbnail((size,size))
                img.paste(logo, (x,y))
        elif field.field == 'photo':
            if participant.photo:
                photo = Image.open(participant.photo)
                photo.thumbnail((size,size))
                img.paste(photo, (x,y))
        else:
            if field.field == 'text':
                content = field.format
            else:
                content = match[field.field]
            fnt = ImageFont.truetype(field.font.filename, size)
            color = field.color
            text = ("%s") % (content)
            textsize = draw.textsize(text, font=fnt)
            if textsize[0]+x < badge_size_x:
                draw.text((x,y), ("%s") % (content), font=fnt, fill=color)
            else:
                # calculate maximum size in characters
                max_chars = (badge_size_x-(x*2)) * len(text) / textsize[0]
                lines = textwrap.fill(text, max_chars).splitlines()
                tmp = y
                for line in lines:
                    draw.text((x,y), line, font=fnt, fill=color)
                    y += size
                y = tmp

    # FIXME: add barcode
    short_full_name = "%s: %s" % (participant.id, participant.short_full_name())
    barcode = get_barcode(short_full_name, badge_size_x-4)
    barcode_image = renderPM.drawToPIL(barcode)
    img.paste(barcode_image, (0+2, badge_size_y-70))

    img.save(where, "PNG")
