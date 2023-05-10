# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.home, name='home'),

    path('reg/employee', views.reg_employee, name='reg_employee'),
    path('reg/client', views.reg_client, name='reg_client'),
    
    path('employee', views.employee, name='employee'),
    path('employee/update/<str:id>', views.update_employee, name='update_employee'),
    path('employee/delete/<str:id>', views.del_employee, name='del_employee'), # Delete confirmation Employee
    
    path('clients', views.client, name='client'),
    path('client/update/<str:id>', views.update_client, name='update_client'),
    path('client/delete/<str:id>', views.del_client, name='del_client'),
    
    path('client/ledger', views.client_ledger, name='client_ledger'),
    path('delete/clientbook/<str:id>', views.del_clientbook_entry, name='del_clientbook'),
    path('update/clientbook/<str:id>', views.update_clientbook_entry, name='update_clientbook'),
    
    path('attendance', views.attendance, name='attendance'),
    path('employee/attendance', views.view_attendance, name='view_attendance'),
    
    path('ledger', views.general_ledger, name='general_ledger'),
    path('delete/ledger/<int:id>', views.del_gl_entry, name='del_gl_entry'),# Delete confirmation of General Ledger Entry
    path('update/ledger/<int:id>', views.update_gl_entry, name='update_gl_entry'), # update entry of General Ledger
    
    path('employee/ledger', views.employee_salarybook, name='employee_ledger'),
    path('update/salarybook/<str:id>', views.update_salarybook_entry, name='update_salarybook'), # update entry of General Ledger
    path('delete/salarybook/<str:id>', views.del_salarybook_entry, name='del_salarybook'),# Delete confirmation of General Ledger Entry
    
    path('employee/profile/<str:id>', views.profile_employee, name='profile_employee'),
    path('client/profile/<str:id>', views.profile_client, name='profile_client'),
    
    path('invoice', views.invoice, name='invoice'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),


]
