# -*- encoding: utf-8 -*-

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

import datetime

from .models import GeneralLedger, SalaryBook, ClientBook,Employee,Client, Attendance
from apps.home import models
from django.db.models import Sum
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.db.models.functions import Coalesce
from django.db.models import F, Sum, Window

# This is for employee login functionality
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user= Authenticate(username= username, password=password)
#         if user != None:
#             login(request, user)
#             return HttpResponseRedirect('profile_employee')
#         else:
#             messeges.error(request, "Login Failed. Please provide correct information")
#             return HttpResponseRedirect('/login/')


@login_required(login_url="/login/")
def home(request):
    emp_count = Employee.objects.all().count()
    client_count = Client.objects.all().count()
    # Total spending data
    gl_spending = GeneralLedger.objects.aggregate(spending__sum=Coalesce(Sum('spending'),0))
    sb_withdraw = SalaryBook.objects.aggregate(withdraw__sum=Coalesce(Sum('withdraw'),0))
    total_spending = gl_spending['spending__sum'] + sb_withdraw['withdraw__sum']
    # Total Earning data
    gl_received = GeneralLedger.objects.aggregate(received__sum=Coalesce(Sum('received'),0))
    sb_payment = ClientBook.objects.aggregate(payment__sum=Coalesce(Sum('payment'), 0))
    total_earning = gl_received['received__sum'] + sb_payment['payment__sum']
    
    context = {'segment': 'home',
               'emp_count': emp_count,
               'client_count':client_count,
               'total_spending':total_spending,
               'total_earning':total_earning,
               }

    return render(request, 'home/index.html', context)


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

    
# View for Employee Registration section
@login_required(login_url="/login/")
def reg_employee(request):
    
    if request.method == "POST":
        id = request.POST.get('id')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        salary = request.POST.get('salary')
        g_name = request.POST.get('g_name')
        g_phone = request.POST.get('g_phone')
        
        employee = Employee(emp_id=id.upper(), name=name, phone=phone, age=age, gender=gender, address=address, salary=salary, g_name=g_name, g_phone=g_phone)
        employee.save()
        return redirect(reverse('employee'))
    return render(request, 'home/employee-register.html')


# View for Client Registration section
@login_required(login_url="/login/")
def reg_client(request):
    if request.method == "POST":
        client_id = request.POST.get('id')
        company_name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        email = request.POST.get('mail')
        
        client = Client(client_id=client_id.upper(), company_name=company_name, phone=phone, address=address, email=email)
        client.save()
        return redirect(reverse('client'))

    return render(request, 'home/client-register.html')

    
# View for Ledger Section
@login_required(login_url="/login/")
def general_ledger(request):
    
    if request.method == "POST":
        id = request.POST.get('user_id')
        date = request.POST.get('date')
        desc = request.POST.get('description')
        debit = int(request.POST.get('received'))
        credit = int(request.POST.get('spending'))
        
        # try:
        entry = GeneralLedger(user_id=id, date=date, description=desc,received=debit, spending=credit)
        entry.save()
        # messages.success(request,"Entry has been saved successfully.")
        return HttpResponseRedirect('/ledger')            
        # except:
        #     print("value error")
        
    
    # Get data from General_Ledger
    try:
        GeneralLedgerData = GeneralLedger.objects.all().order_by("date")
        Total = GeneralLedger.objects.aggregate(Sum('received'), Sum('spending'))
    except:
        return HttpResponse("505 Not Found")
    
    paginator = Paginator(GeneralLedgerData, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'segment': 'ledger',
        'total': Total,
    }
    
    # initial request would get the last page
    if not page_number:
        return redirect(f'/ledger?page={paginator.num_pages}')
    
    return render(request, 'home/ledger.html', context)

    
# class based view for the ledger page
# class LedgerListView(ListView):
#     model = GeneralLedger
#     template_name = 'home/tables.html'
#     paginate_by = 30
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['records'] = GeneralLedger.objects.all()
#         context['segment'] = 'ledger'
#         return context

# Update General ledger data -----------------------------------------------
def update_gl_entry(request,id): 
    record = GeneralLedger.objects.get(id=id)
    
    if request.method == 'POST':
            record.user_id = request.POST.get('user_id')
            record.date = request.POST.get('date')
            record.description = request.POST.get('description')
            record.received = request.POST.get('received')
            record.spending = request.POST.get('spending')
        
            record.save()
            return redirect('general_ledger')
    context = {
        'record':record
    }
    return render(request, 'forms/update-ledger.html', context)

# Delete General ledger data-----------------------------------------------
@login_required(login_url="/login/")
def del_gl_entry(request, id):
    record = GeneralLedger.objects.get(id=id)
    context = {'record':record}
    if request.method == 'POST':
        record.delete()
        return redirect('general_ledger')
    return render(request, 'confirm/ledger-delete.html', context)


# Employee SalaryBook starts here ------------------------------------------------
@login_required(login_url="/login/")
def employee_salarybook(request):
    
    if request.method == "POST":
        id = request.POST.get('emp_id')
        employee = Employee.objects.get(emp_id=id)
        date = request.POST.get('date')
        desc = request.POST.get('description')
        withdraw = int(request.POST.get('withdraw'))
       
        # try:
        entry = SalaryBook(employee=employee, date=date, description=desc,withdraw=withdraw)
        entry.save()
        messages.success(request,"Entry has been saved successfully.")
        return HttpResponseRedirect('/employee/ledger')            
        # except:
        #     print("value error")
        
    
    # Get data from  Salary book
    employees = Employee.objects.all() 
    SalaryBookData = SalaryBook.objects.all().order_by("date")
    paginator = Paginator(SalaryBookData, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'employees':employees,
        'segment': 'salarybook',
    }
    
    # initial request would get the last page
    if not page_number:
        return redirect(f'/employee/ledger?page={paginator.num_pages}')
    
    return render(request, 'home/employee-ledger.html', context)   
# Employee SalaryBook ends here ------------------------------------------------

# Update SalaryBook starts from here ------------------------------------------
def update_salarybook_entry(request,id):
    record = SalaryBook.objects.get(id=id)
    
    if request.method == 'POST':
            record.date = request.POST.get('date')
            record.description = request.POST.get('description')
            record.withdraw = request.POST.get('withdraw')
        
            record.save()
            return redirect('employee_ledger')
    context = {
        'record':record
    }
    return render(request, 'forms/update-salarybook.html', context)

# Delete SalaryBook entry -----------------------------------
@login_required(login_url="/login/")
def del_salarybook_entry(request, id):
    record = SalaryBook.objects.get(id=id)
    context = {'record':record}
    if request.method == 'POST':
        record.delete()
        return redirect('employee_ledger')
    return render(request, 'confirm/delete-salarybook.html', context)


# View for Employee section
@login_required(login_url="/login/")
def employee(request):
    # Get data from Employee_Ledger
    EmployeeData = Employee.objects.all().order_by('name')
    context = {
        'employees': EmployeeData,
        'segment': 'employee'
    }
    return render(request, 'home/employee.html', context)
# Update Employee data -----------------------------------------------
def update_employee(request,id):
    employee = Employee.objects.get(emp_id=id)
    
    if request.method == 'POST':
        employee.emp_id = request.POST.get('id')
        employee.name = request.POST.get('name')
        employee.phone = request.POST.get('phone')
        employee.age = request.POST.get('age')
        employee.address = request.POST.get('address')
        employee.gender = request.POST.get('gender')
        employee.salary = request.POST.get('salary')
        employee.g_name = request.POST.get('g_name')
        employee.g_phone = request.POST.get('g_phone')
        
        employee.save()
        return redirect('employee')
    
    context = {
        'employee':employee
    }
    return render(request, 'forms/update-employee.html', context)

@login_required(login_url="/login/")
def del_employee(request, id):
    employee = Employee.objects.get(emp_id=id)
    context = {'employee':employee}
    if request.method == 'POST':
        employee.delete()
        return redirect('employee')
    return render(request, 'confirm/delete-employee.html', context)

# View for Client section
@login_required(login_url="/login/")
def client(request):
    # Get data from Client
    ClientData = Client.objects.values()
    context = {
        'clients': ClientData,
        'segment': 'client'
    }
    return render(request, 'home/clients.html', context)

# Update Employee data -----------------------------------------------
def update_client(request,id):
    client = Client.objects.get(client_id=id)
    
    if request.method == 'POST':
        client.client_id = request.POST.get('id')
        client.company_name = request.POST.get('name')
        client.phone = request.POST.get('phone')
        client.address = request.POST.get('address')
        client.email = request.POST.get('mail')
        
        client.save()
        return redirect('client')
    
    context = {
        'client':client
    }
    return render(request, 'forms/update-client.html', context)

@login_required(login_url="/login/")
def del_client(request, id):
    client = Client.objects.get(client_id=id)
    context = {'client':client}
    if request.method == 'POST':
        client.delete()
        return redirect('client')
    return render(request, 'confirm/delete-client.html', context)

# Clients ClientBook starts here ------------------------------------------------
@login_required(login_url="/login/")
def client_ledger(request):    
    # if request.method == "POST":
    #     id = request.POST.get('client_id')
    #     client= Client.objects.get(client_id=id)
    #     date = request.POST.get('date')
    #     desc = request.POST.get('description')
    #     quantity = int(request.POST.get('quantity'))
    #     unit_price = float(request.POST.get('unit_price'))
    #     payment = int(request.POST.get('payment'))
    
    #     entry = ClientBook(client=client,date=date,description=desc,quantity=quantity,unit_price=unit_price,payment=payment)
    #     entry.save()
    #     messages.success(request,"Entry has been saved successfully.")
    #     return HttpResponseRedirect('/client/ledger')            
    
    # Get data from  Salary book
    clients = Client.objects.all() 
    ClientBookData = ClientBook.objects.all()
    paginator = Paginator(ClientBookData, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'clients':clients,
        'segment': 'clientbook',
    }
    
    # initial request would get the last page
    if not page_number:
        return redirect(f'/client/ledger?page={paginator.num_pages}')
    
    return render(request, 'home/client-ledger.html', context)   

# Update Client starts from here ------------------------------------------
def update_clientbook_entry(request,id):
    record = ClientBook.objects.get(id=id)
    
    if request.method == 'POST':
            record.date = request.POST.get('date')
            record.description = request.POST.get('description')
            record.quantity = int(request.POST.get('quantity'))
            record.unit_price = float(request.POST.get('unit_price'))
            record.payment = int(request.POST.get('payment'))
            record.total_price = record.quantity * record.unit_price
        
            record.save()
            return redirect('client_ledger')
    context = {
        'record':record
    }
    return render(request, 'forms/update-clientbook.html', context)

@login_required(login_url="/login/")
def del_clientbook_entry(request, id):
    record = ClientBook.objects.get(id=id)
    context = {'record':record}
    if request.method == 'POST':
        record.delete()
        return redirect('client_ledger')
    return render(request, 'confirm/delete-clientbook.html', context)


@login_required()
def attendance(request):
    EmployeeData = Employee.objects.values('emp_id', 'name')
    if request.method == "POST":
        date = request.POST.get('date') #datetime.strptime(post['attendance_date'], '%Y-%m-%d')
        
        for emp in EmployeeData:
            employee = Employee.objects.get(emp_id = emp['emp_id'])
            get_status = request.POST.get(emp['emp_id'])
            if get_status == 'present':
                status = 1
            else:
                status = 0
            try:    
                attendance = Attendance(employee=employee, date=date, status=status)
                attendance.save()
            except:
                print("IntegrityError")
        return render(request, 'home/index.html')
      
    context = {
        'employees': EmployeeData,
        'segment': 'attendance',
    }
    return render(request, 'attend/attendance.html', context)

# For viewing all employees monthly attendance sheet
def view_attendance(request):
    
    if request.method == 'POST':
        get_date = request.POST.get('date')
        date = datetime.datetime.strptime(get_date, '%Y-%m')
        year = date.year
        month = date.month
        start_date = datetime.date(year, month, 1)
        if (month == 12):
            end_date = datetime.date(year+1, 1, 1) - datetime.timedelta(days=1)
        else:
            end_date = datetime.date(year, month+1, 1) - datetime.timedelta(days=1)
        #Get data from the attendance sheet of the specified month
        attendance_records = Attendance.objects.filter( date__range=(start_date, end_date))
        day_count = int((end_date - start_date).days) + 2

        employee_attendance = {}
        # Loop through each attendance record and store it in the dictionary
        for attendance in attendance_records:
            if attendance.employee not in employee_attendance:
                employee_attendance[attendance.employee] = {}

            employee_attendance[attendance.employee][attendance.date.day] = attendance.status
        context = {
        'employee_attendance': employee_attendance,
        'month': date,
        'day_count': range(1,day_count),
        'segment':'attendance sheet',
        }
        return render(request, 'attend/attend_sheet.html', context)
    
        
    # extracting current Year and month 
    today = datetime.date.today()
    year = today.year
    month = today.month

    # Create a datetime object representing the start and end of the month
    start_date = datetime.date(year, month, 1)
    if (month == 12):
        end_date = datetime.date(year+1, 1, 1) - datetime.timedelta(days=1)
    else:
        end_date = datetime.date(year, month+1, 1) - datetime.timedelta(days=1)

    # Filter the Attendance model to retrieve all the attendance for the employee in the specified month
    attendance_records = Attendance.objects.filter( date__range=(start_date, end_date))

    employee_attendance = {}

    # Loop through each attendance record and store it in the dictionary
    for attendance in attendance_records:
        if attendance.employee not in employee_attendance:
            employee_attendance[attendance.employee] = {}

        employee_attendance[attendance.employee][attendance.date.day] = attendance.status

    day_count = int((end_date - start_date).days) + 2
    
    context = {
        'employee_attendance': employee_attendance,
        'month': today,
        'day_count': range(1,day_count),
        'segment':'attendance sheet',
    }
    return render(request, 'attend/attend_sheet.html', context)

# This is for employee profile view       (Incomplete)
@login_required(login_url="/login/")
def profile_employee(request, id):
    employee = Employee.objects.get(emp_id=id)
       
    if request.method == "POST":
        get_date = request.POST.get('date')
        date = datetime.datetime.strptime(get_date, '%Y-%m')
        year,month = date.year,date.month
        start_date = datetime.date(year, month, 1)
        if (month == 12):
            end_date = datetime.date(year+1, 1, 1) - datetime.timedelta(days=1)
        else:
            end_date = datetime.date(year, month+1, 1) - datetime.timedelta(days=1)
        #Get data from the attendance sheet of the specified month
        SalaryBookData = SalaryBook.objects.filter(employee=employee,date__range=(start_date, end_date))
        total = SalaryBookData.aggregate(sum=Sum('withdraw'))
        
        context = {
            'employee':employee,
            'page_obj': SalaryBookData,
            'total': total,
        }
        return render(request, 'home/profile-employee.html', context)

    today = datetime.date.today()
    year = today.year
    # Create a datetime object representing the start and end of the month
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year+1, 1, 1) - datetime.timedelta(days=1)

    # Filter the Attendance model to retrieve all the attendance for the employee in the specified month
    attendance_records = Attendance.objects.filter(employee=employee, date__range=(start_date, end_date))

    employee_attendance = {}

    # Loop through each attendance record and store it in the dictionary
    for attendance in attendance_records:
        if attendance.date.strftime("%b") not in employee_attendance:
            employee_attendance[attendance.date.strftime("%b")] = {}
        employee_attendance[attendance.date.strftime("%b")][attendance.date.day] = attendance.status

    day_count = int((end_date - start_date).days) + 2
    #---------------------------------------------------
    
    SalaryBookData = SalaryBook.objects.filter(employee=employee).order_by("date")
    total = SalaryBookData.aggregate(sum=Sum('withdraw'))
    paginator = Paginator(SalaryBookData, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'employee':employee,
        'page_obj': page_obj,
        'total': total,
        'segment': 'employee-profile',
        'employee_attendance': employee_attendance,
        'day_count':day_count,
        'year':today,
    }
    
    # initial request would get the last page
    if not page_number:
        return redirect(f'/employee/profile/{id}?page={paginator.num_pages}')
    
    return render(request, 'home/profile-employee.html', context)


# This is for employee profile view
@login_required(login_url="/login/")
def profile_client(request, id):
    
    if request.method == "POST":
        client= Client.objects.get(client_id=id)
        date = request.POST.get('date')
        desc = request.POST.get('description')
        quantity = int(request.POST.get('quantity'))
        unit_price = float(request.POST.get('unit_price'))
        total_price = quantity * unit_price
        payment = int(request.POST.get('payment'))
    
        entry = ClientBook(client=client,date=date,description=desc,quantity=quantity,unit_price=unit_price,total_price=total_price,payment=payment)
        entry.save()
        messages.success(request,"Entry has been saved successfully.")
        return HttpResponseRedirect(f'/client/profile/{id}')            
    
    
    # Get data from  Salary book
    client = Client.objects.get(client_id=id)
    ClientBookData = ClientBook.objects.filter(client=client).annotate(
        cumbalance=Window(expression = Sum('total_price'),order_by=F('id').asc()) - Window(expression = Sum('payment'), order_by=F('id').asc())
    )
    paginator = Paginator(ClientBookData, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'client':client,
        'segment': 'clientprofile',
    }
    # initial request would get the last page
    if not page_number:
        return redirect(f'/client/profile/{id}?page={paginator.num_pages}')
    return render(request, 'home/profile-client.html', context)


def invoice(request):    
    return render(request, "invoice/ledger-invoice.html")