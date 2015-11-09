from django.core.management.base import BaseCommand, CommandError
from forocacao.app.models import Attendee, AttendeeType, Event
from forocacao.app.png import createPNG

class Command(BaseCommand):
    help = 'Generates JPEG badges for all attendees'

    def add_arguments(self, parser):
        parser.add_argument('event_id', type=int)
        parser.add_argument('type_id', type=int)

    def handle(self, *args, **options):

        event_id = options['event_id']
        type_id = options['type_id']

        try:
            attendees = Attendee.objects.filter(event_id=event_id, type_id=type_id, approved=True)
            for attendee in attendees:
                filename = "%s.png" % (attendee.username,)
                print attendee
                createPNG(attendee, filename)
        except AttendeeType.DoesNotExist:
            raise CommandError('type "%s" does not exist' % type_id)
        except Event.DoesNotExist:
            raise CommandError('event "%s" does not exist' % event_id)

        self.stdout.write('Successfully generate %s badges for event "%s"' % (len(attendees), event_id))
