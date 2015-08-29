from django.conf import settings

from forocacao.app.models import Event, Content

def get_or_none(model, objects, *args, **kwargs):
    try:
        return objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None

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
            'current_info': get_or_none(Content, current_event.contents, page='info'),
            'current_footer': get_or_none(Content, current_event.contents, page='footer'),
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
