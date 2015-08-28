from django.conf import settings

from forocacao.app.models import Event

def current_event(request):
    '''
    A context processor to add the "current event" to the current Context
    '''
    try:
        current_event = Event.objects.filter(status='frontpage')[0]
        return {
            'current_event': current_event.name,
            'current_slug': current_event.slug,
            'current_footer': current_event.contents.get(page='footer'),
        }
    except Event.DoesNotExist:
        # always return a dict, no matter what!
        return {
            'current_event': '',
            'current_slug': '',
            'current_footer': '',
        }
