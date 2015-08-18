from django.contrib import admin
from .models import Event, Activity, Profession, Attendee


class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class ActivityAdmin(admin.ModelAdmin):
    list_filter = ('event__name',)
    prepopulated_fields = {"slug": ("name",)}

class ProfessionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('event__name',)

class AttendeeAdmin(admin.ModelAdmin):
    list_filter = ('event__name',)
    fieldsets = (
    	(None, {
            'fields': ('event','type','first_name', 'last_name', 'email', 'profession',
		'phone','age','country','document','photo')
        }),
        ('Informacion de actividades y biografia', {
            'classes': ('collapse',),
            'fields': ('text','activities',)
    	}),
        ('Permisos de usuario', {
            'classes': ('collapse',),
            'fields': ('name','username', 'password', 'is_active','is_staff','is_superuser','groups','user_permissions','last_login','date_joined')
    	}),
    )

admin.site.register(Event, EventAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(Attendee, AttendeeAdmin)
