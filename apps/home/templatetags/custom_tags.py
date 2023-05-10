from django import template
from datetime import datetime

register = template.Library()


@register.filter
def get_item(dictionary,key):
    return dictionary.get(key)

@register.filter
def get_range(num):
    return range(1,int(num))

@register.filter
def multiply(a, b):
    return a * b

@register.filter
def get_valuecount(dictionary):
    return sum(dictionary.values())

@register.filter
def get_weekday(dates, day):
    week = datetime(dates.year,dates.month,day)
    return week.strftime('%a')