from django.contrib import admin
from django import forms

from .models import Event, Activity, Profession, Attendee, AttendeeType, PaymentMethod

class AttendeeTypeInline(admin.TabularInline):
    model = Event.types.through

class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        AttendeeTypeInline,
    ]

class ActivityAdmin(admin.ModelAdmin):
    list_filter = ('event__name',)
    prepopulated_fields = {"slug": ("name",)}

class ProfessionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    #list_filter = ('event__name',)

def has_approval_permission(request, obj=None):
    if request.user.has_perm('users.can_approve_participant'):
        return True
    return False

class AttendeeAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email','profession']
    list_filter = ('event__name','country','profession','type')
    search_fields = ['id','first_name','last_name']

    fieldsets = (
    	(None, {
            'fields': ('event','type','first_name', 'last_name', 'email', 'profession',
            'phone','country','nationality','sponsored','sponsor','payment_method','photo')
        }),
        ('Informacion de actividades y biografia', {
            'classes': ('collapse',),
            'fields': ('text','activities',)
    	}),
        ('Permisos de usuario', {
            'classes': ('collapse',),
            'fields': ('username', 'password', 'is_active','last_login','date_joined')
    	}),
    )

    def get_queryset(self, request):
        qs = super(AttendeeAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(event=request.user.event)

    def get_form(self, request, obj=None, **kwargs):
        if not has_approval_permission(request, obj):
            print "you DO NOT have permission"
            self.fieldsets = (
                (None, {
                    'fields': ('event','type','first_name', 'last_name', 'email', 'profession',
                    'phone','country','nationality','sponsored','sponsor','payment_method','photo')
                }),
                ('Informacion de actividades y biografia', {
                    'classes': ('collapse',),
                    'fields': ('text','activities',)
                }),
                ('Permisos de usuario', {
                    'classes': ('collapse',),
                    'fields': ('username', 'password', 'last_login','date_joined')
                }),
            )
        form = super(AttendeeAdmin, self).get_form(request, obj, **kwargs)

        # required fields (not required in original model)
        form.base_fields['first_name'].required = True
        form.base_fields['last_name'].required = True
        form.base_fields['email'].required = True

        # if update, limit type and profession to current event
        if obj:
            form.base_fields['profession'].queryset = Profession.objects.filter(id__in=obj.event.professions.all())
            form.base_fields['type'].queryset = AttendeeType.objects.filter(id__in=obj.event.types.all())
            form.base_fields['payment_method'].queryset = PaymentMethod.objects.filter(id__in=obj.event.payment_methods.all())

        # if not superuser, limit type and profession to user's event
        if not request.user.is_superuser:
            form.base_fields['profession'].queryset = Profession.objects.filter(id__in=request.user.event.professions.all())
            form.base_fields['type'].queryset = AttendeeType.objects.filter(id__in=request.user.event.types.all())
            form.base_fields['payment_method'].queryset = PaymentMethod.objects.filter(id__in=request.user.event.payment_methods.all())
            form.base_fields['event'].initial = request.user.event
            form.base_fields['event'].widget = forms.HiddenInput()
            form.base_fields['event'].label = ''
            #self.readonly_fields = ('event',)
        return form

admin.site.register(Event, EventAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(PaymentMethod)
