from django.conf import settings

from forocacao.app.models import Event, Content

def get_or_none(model, objects, *args, **kwargs):
    try:
        return objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None

def google_analytics(request):
    '''
    A context processor to access Google Analytics data
    '''
    return {
            'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY,
    }

def current_event(request):
    '''
    A context processor to add the "current event" to the current Context
    '''
    events = Event.objects.all()
    try:
        basehtml = 'base.html'
        if (hasattr(request, 'resolver_match') and request.resolver_match) and (request.resolver_match.kwargs.get('eventslug') or request.resolver_match.kwargs.get('slug')):
            slug = request.resolver_match.kwargs.get('eventslug') or request.resolver_match.kwargs.get('slug')
            if slug and slug.endswith('/'):
                slug = slug[:-1]
            current_event = Event.objects.get(slug=slug)
        else:
            current_event = Event.objects.filter(status='frontpage')[0]
        if current_event.template:
            basehtml = current_event.template

        return {
            'events': events,
            'event': current_event,
            'basehtml': basehtml,
            'current_event': current_event.name,
            'current_slug': current_event.slug,
            'current_info': get_or_none(Content, current_event.contents, page='info'),
            'current_footer': get_or_none(Content, current_event.contents, page='footer'),
        }
    except Event.DoesNotExist:
        # always return a dict, no matter what!
        return {
            'events': events,
            'event': None,
            'basehtml': 'base.html',
            'current_event': '',
            'current_slug': '',
            'current_info': '',
            'current_footer': '',
        }
