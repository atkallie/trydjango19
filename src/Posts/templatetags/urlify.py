# -*- coding: utf-8 -*-

# Need the above line to include comments in file

# To be a valid tag library, the module must contain a module-level variable named register that is a template.Library
# instance, in which all the tags and filters are registered
from django import template
from urllib import quote_plus

register = template.Library()

# Custom filters are simply Python functions that take one or two parameters, a variable value and an (optional) argument

@register.filter
def urlify(value):
    return quote_plus(value)

#since no 'name' argument is specified (i.e. @register.filter(name='someName'))
# Django will use the function’s name as the filter name

# You then load this module in the HTML template where you wish to use it by entering {% load urlify %}
# And use it by typing {{ singleObj.content|urlify }}
# Note how singleObj.content is passed as the variable value in the filter (function) definition above