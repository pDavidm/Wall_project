import datetime
from django import template

register = template.Library()

@register.filter
def min_ago(time, minuets):
    return time + datetime.timedelta(minuets=minuets) < datetime.datetime.now()