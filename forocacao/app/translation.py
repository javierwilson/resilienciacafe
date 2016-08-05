from modeltranslation.translator import translator, TranslationOptions
from .models import Event, Content


class EventTranslationOptions(TranslationOptions):
    fields = ('name', 'title',)

translator.register(Event, EventTranslationOptions)


class ContentTranslationOptions(TranslationOptions):
    fields = ('name', 'title', 'text')

translator.register(Content, ContentTranslationOptions)
