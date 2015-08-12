from django.contrib import admin
from .models import Conference, Activity, Profession, Attendee


class ConferenceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class ActivityAdmin(admin.ModelAdmin):
    list_filter = ('conference__name',)
    prepopulated_fields = {"slug": ("name",)}

class ProfessionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('conference__name',)

class AttendeeAdmin(admin.ModelAdmin):
    list_filter = ('conference__name',)

admin.site.register(Conference, ConferenceAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(Attendee, AttendeeAdmin)