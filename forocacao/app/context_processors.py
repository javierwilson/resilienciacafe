from django.conf import settings

from forocacao.app.models import Event

def current_event(request):
    '''
    A context processor to add the "current event" to the current Context
    '''
    try:
        current_event = Event.objects.filter(status='frontpage')[0]
        return {
            'event': current_event,
            'current_event': current_event.name,
            'current_slug': current_event.slug,
            'current_info': current_event.contents.get(page='info'),
            'current_footer': current_event.contents.get(page='footer'),
        }
    except Event.DoesNotExist:
        # always return a dict, no matter what!
        return {
            'event': None,
            'current_event': '',
            'current_slug': '',
            'current_info': '',
            'current_footer': '',
        }
