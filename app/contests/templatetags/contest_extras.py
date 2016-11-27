from django import template

# Allow get list item in template
register = template.Library()
@register.filter
def index(sequence, position):
	return sequence[position-1]
