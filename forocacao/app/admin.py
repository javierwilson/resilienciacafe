from django.contrib import admin
from .models import Conference, Activity, Profession, AttendeeType, Attendee


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
    fieldsets = (
    	(None, {
            'fields': ('conference','attendee_type','first_name', 'last_name', 'email', 'profession',
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

class AttendeeTypeAdmin(admin.ModelAdmin):
    list_filter = ('conference__name',)

admin.site.register(Conference, ConferenceAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(AttendeeType, AttendeeTypeAdmin)
admin.site.register(Attendee, AttendeeAdmin)
