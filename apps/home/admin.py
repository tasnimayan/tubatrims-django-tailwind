# -*- encoding: utf-8 -*-

from django.contrib import admin


from .models import GeneralLedger, Employee, SalaryBook, Client, ClientBook, Attendance


# This section is for changing the Admin page details
admin.site.site_title = "TubaTrims"
admin.site.site_header = "Tuba Trims Administration"
admin.site.index_title = "Manage Database"

# This section is for changing the model tables in the admin page
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'name', 'phone', 'address', 'salary')
    search_fields = ('name',)
    
    # Make the table fields editable in the table form
    # list_editable = ('name', 'phone', 'address', 'salary')
    
    
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'company_name', 'phone', 'address')
    search_fields = ('company_name',)
    
    
class GeneralLedgerAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'received', 'spending')
    search_fields = ('date',)

    
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status')
    search_fields = ('date',)
    
    # Make the table fields editable in the table form
    list_editable = ('date', 'status')   


# Register your models here.
admin.site.register(GeneralLedger, GeneralLedgerAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(SalaryBook)
admin.site.register(Client, ClientAdmin)
admin.site.register(ClientBook)
admin.site.register(Attendance, AttendanceAdmin)

