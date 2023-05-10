# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.
class GeneralLedger(models.Model):
    user_id = models.CharField(max_length=20, default='admin')
    date = models.DateField()
    description = models.TextField(null=False)
    received = models.IntegerField(null=True)
    spending = models.IntegerField(null=True)
    
    class Meta:
        ordering = ['id']


# Employee profile create
class Employee(models.Model):
    emp_id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    age = models.PositiveIntegerField()
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    address = models.CharField(max_length=100)
    salary = models.IntegerField()
    g_name = models.CharField(max_length=50, null=True, )
    g_phone = models.CharField(max_length=15, null=True)
    
    def __str__(self):
        return self.emp_id
    
# Employee Salary Book   
class SalaryBook(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    date = models.DateField()
    description = models.TextField(null=True)
    withdraw = models.IntegerField()
    
    class Meta:
        ordering = ['id']
    
    
# Client profile create
class Client(models.Model):
    client_id = models.CharField(primary_key=True, max_length=20)
    company_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    
    def __str__(self):
        return self.client_id
    
# Client Ledger Book
class ClientBook(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    date = models.DateField()
    description = models.TextField(null=True)
    quantity = models.IntegerField(default=0, null=True)
    unit_price = models.FloatField(default=0, null=True)
    total_price = models.FloatField()
    payment = models.IntegerField(default=0, null=True)
    
    
    def __str__(self):
        return str(self.client) +" "+ str(self.date)
    
    class Meta:
        ordering = ['id']
    
       
# This model for Attendance database of Emplyees
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ["employee", "date"]  
    def __str__(self):
        return str(self.employee)