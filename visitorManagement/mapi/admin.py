from django.contrib.gis import admin
from visitorManagement.mapi.models import Member, Visitor, WorkBookType, WorkBook
from visitorManagement.mapi.form import WorkBookTypeAdminForm


class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_active', 'mobile_no')
    list_filter = ('is_active',)
    search_fields = ('id', 'name', 'email', 'mobile_no')

    def get_actions(self, request):
        actions = super(MemberAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


class VisitorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mobile_no', 'vehicle_no', 'from_place',
                    'destination_place', 'in_time', 'out_time')
    search_fields = ('id', 'name', 'mobile_no', 'vehicle_no', 'from_place', 'destination_place',
                     'in_time', 'out_time')  # todo handle filter on in-time and out-time

    def get_actions(self, request):
        actions = super(VisitorAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


class WorkBookTypeAdmin(admin.ModelAdmin):
    #form = WorkBookTypeAdminForm
    list_display = ('type', 'mandatory_fields')

    def get_actions(self, request):
        actions = super(WorkBookTypeAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        super(WorkBookTypeAdmin, self).save_model(request, obj, form, change)


class WorkBookAdmin(admin.ModelAdmin):
    list_display = ('wb_name', 'wb_type', 'member')

    def get_actions(self, request):
        actions = super(WorkBookAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Member, MemberAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(WorkBookType, WorkBookTypeAdmin)
admin.site.register(WorkBook, WorkBookAdmin)
