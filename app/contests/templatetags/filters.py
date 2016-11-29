from django import template
from django.utils.safestring import mark_safe
from django.forms import CheckboxInput
from django.forms import CheckboxSelectMultiple
import re

'''
register = template.Library()

class_re = re.compile(r'(?<=class=["\'])(.*)(?=["\'])')

@register.filter(name='label_add_class')
def add_class(value, css_class):
    string = unicode(value)
    match = class_re.search(string)
    if match:
        m = re.search(r'^%s$|^%s\s|\s%s\s|\s%s$' % (css_class, css_class,
                                                    css_class, css_class),
                                                    match.group(1))
        print match.group(1)
        if not m:
            return mark_safe(class_re.sub(match.group(1) + " " + css_class, string))
    else:
        if('/>' in string):
            return mark_safe(string.replace('/>', ' class="%s" />' % css_class, 1))
        else:
            return mark_safe(string.replace('>', ' class="%s">' % css_class, 1))
    return value

@register.filter(name='is_checkbox')
def is_checkbox(field):
  return (field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__ or
  field.field.widget.__class__.__name__ == CheckboxSelectMultiple().__class__.__name__)
'''