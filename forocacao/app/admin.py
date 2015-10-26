from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.core.mail import send_mail, EmailMessage
from django.utils.translation import ugettext as _

from suit_redactor.widgets import RedactorWidget
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportMixin


from .models import Event, Activity, Profession, Invited, Attendee, AttendeeType, AttendeePayment, PaymentMethod, EventBadge, Font, AttendeeReceipt, Content, Field
from .pdf import createPDF

def has_approval_permission(request, obj=None):
    if request.user.has_perm('users.can_approve_participant'):
        return True
    return False


class ContentForm(forms.ModelForm):
    class Meta:
        widgets = {
            'text': RedactorWidget(editor_options={'lang': 'es', 'minHeight': '300'})
        }

class ContentAdmin(admin.ModelAdmin):
    form = ContentForm

admin.site.register(Content, ContentAdmin)

class AttendeeTypeInline(admin.TabularInline):
    model = Event.types.through

class EventBadgeInline(admin.TabularInline):
    model = EventBadge

class AttendeePaymentInline(admin.TabularInline):
    model = AttendeePayment

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "payment_method":
            if self.parent_obj and self.parent_obj.event:
                kwargs["queryset"] = PaymentMethod.objects.filter(id__in=self.parent_obj.event.payment_methods.all())
            if not request.user.is_superuser:
                kwargs["queryset"] = PaymentMethod.objects.filter(id__in=request.user.event.payment_methods.all())
        return super(AttendeePaymentInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super(AttendeePaymentInline, self).get_formset(
            request, obj, **kwargs)

class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        AttendeeTypeInline,
        EventBadgeInline,
    ]

class ActivityAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class ProfessionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class AttendeeReceiptAdmin(admin.ModelAdmin):
    list_display = ['attendee', 'date' ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(AttendeeReceiptAdmin, self).get_form(request, obj, **kwargs)

        # if not superuser, limit type and profession to user's event
        if not request.user.is_superuser:
            form.base_fields['attendee'].queryset = Attendee.objects.filter(id__in=request.user.event.user_set.all())

        # show balance
        form.base_fields['attendee'].label_from_instance = lambda obj: "%s %s (%s %s)" % (obj.first_name, obj.last_name, _('Balance'), obj.balance())

        return form


class AttendeePaymentAdmin(admin.ModelAdmin):
    list_display = ['attendee', 'payment_method', 'amount' ]


class FontResource(resources.ModelResource):
    class Meta:
        model = Font

class InvitedResource(resources.ModelResource):
    class Meta:
        model = Invited
        #fields = ('id', 'first_name', 'last_name', 'organization', 'email')

class AttendeeResource(resources.ModelResource):
    class Meta:
        model = Attendee
        fields = ('id', 'first_name', 'last_name', 'document', 'organization', 'position', 'telephone', 'username', 'email', 'country', 'address', 'sex')

def mail_attendee(modeladmin, request, queryset):
    for obj in queryset:
        message = "%s\r\n%s" % (obj.event.title, obj.event.pdfnote)
        email = EmailMessage(obj.event.name, message, settings.DEFAULT_FROM_EMAIL, [ obj.email ],
                headers={'Message-ID': "%s-%s" % (obj.event.slug, obj.id) })
        filename = '/tmp/%s.pdf' % (obj.email, )
        createPDF(obj, filename)
        email.attach_file(filename)
        email.send()
mail_attendee.short_description = _("Mail selected attendees")

def make_rejected(modeladmin, request, queryset):
    queryset.update(rejected=True)
    for obj in queryset:
        message = "%s\r\n%s" % (obj.event.title, obj.event.reject_note)
        send_mail(obj.event.name, message, settings.DEFAULT_FROM_EMAIL, [ obj.email ])
make_rejected.short_description = _("Reject participation of selected attendees")

def make_approved(modeladmin, request, queryset):
    queryset.update(approved=True)
make_approved.short_description = _("Approve participation of selected attendees")

class InvitedFilter(SimpleListFilter):
    title = _('invited')
    parameter_name = 'invited'

    def lookups(self, request, model_admin):
        return [(True, _('Yes')), (False, _('No'))]

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(email__in=Invited.objects.values('email'))
        elif self.value() == 'False':
            return queryset.exclude(email__in=Invited.objects.values('email'))
        else:
            return queryset

class AttendeeForm(forms.ModelForm):
    class Meta:
        widgets = {
            'text': RedactorWidget(editor_options={'lang': 'es', 'minHeight': '300'})
        }

class AttendeeAdmin(ImportExportModelAdmin):

    form = AttendeeForm

    actions = [make_approved, make_rejected, mail_attendee]

    list_display = ['id','first_name','last_name','email','organization','approved', 'invited', 'rejected']

    resource_class = AttendeeResource

    def my_url_field(self, obj):
        return '<a href="%s%s">%s</a>' % ('http://url-to-prepend.com/', obj.url_field, obj.url_field)
    my_url_field.allow_tags = True
    my_url_field.short_description = 'Column description'

    list_filter = ('event__name','country','organization','type','approved', InvitedFilter, 'rejected')
    search_fields = ['id','first_name','last_name']

    inlines = [
        AttendeePaymentInline,
    ]

    fieldsets = (
        (None, {
            'fields': ('event','type','first_name', 'last_name', 'email', 'approved', 'profession',
            'organization','position','document',
            'phone','country','nationality','extra','sponsored','sponsor','photo')
        }),
        ('Informacion de actividades y biografia', {
            'classes': ('collapse',),
            'fields': ('text','activities',)
        }),
        ('Permisos de usuario', {
            'classes': ('collapse',),
            'fields': ['username', 'password', 'is_active','last_login','date_joined']
        }),
    )

    def get_queryset(self, request):
        qs = super(AttendeeAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(event=request.user.event)

    def get_form(self, request, obj=None, **kwargs):
        if not has_approval_permission(request, obj):
            self.fieldsets[0][1]['fields'] = ('event','type','first_name', 'last_name', 'email', 'approved', 'profession',
                'organization','position','document',
                'phone','country','nationality','extra','sponsored','sponsor','photo')
        form = super(AttendeeAdmin, self).get_form(request, obj, **kwargs)

        # required fields (not required in original model)
        form.base_fields['first_name'].required = True
        form.base_fields['last_name'].required = True
        form.base_fields['email'].required = True
        form.base_fields['password'].required = False
        form.base_fields['username'].required = False

        # if update, limit type and profession to current event
        if obj and obj.event:
            form.base_fields['profession'].queryset = Profession.objects.filter(id__in=obj.event.professions.all())
            form.base_fields['activities'].queryset = Activity.objects.filter(id__in=obj.event.activities.all())
            form.base_fields['type'].queryset = AttendeeType.objects.filter(id__in=obj.event.types.all())

        # if not superuser, limit type and profession to user's event
        if not request.user.is_superuser:
            form.base_fields['profession'].queryset = Profession.objects.filter(id__in=request.user.event.professions.all())
            form.base_fields['activities'].queryset = Activity.objects.filter(id__in=request.user.event.activities.all())
            form.base_fields['type'].queryset = AttendeeType.objects.filter(id__in=request.user.event.types.all())
            form.base_fields['event'].initial = request.user.event
            form.base_fields['event'].widget = forms.HiddenInput()
            form.base_fields['event'].label = ''
            #self.readonly_fields = ('event',)

        return form

    def save_model(self, request, obj, form, change):
        if not obj.username:
            obj.username = obj.email
        obj.save()


class FontAdmin(ImportExportModelAdmin):
    resource_class = FontResource

class InvitedAdmin(ImportExportModelAdmin):
    resource_class = InvitedResource



admin.site.register(Event, EventAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(AttendeeType)
admin.site.register(AttendeePayment, AttendeePaymentAdmin)
admin.site.register(AttendeeReceipt, AttendeeReceiptAdmin)
admin.site.register(PaymentMethod)
admin.site.register(Font, FontAdmin)
admin.site.register(Field)
admin.site.register(Invited, InvitedAdmin)
