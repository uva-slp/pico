from django import template

# Allow get list item in template
register = template.Library()
@register.filter
def index(sequence, position):
	return sequence[position-1]


@register.filter
def print_file_content(f):
	if not f.name:
		return ''
	else:
		try:
			output = f.read()
			return output.encode('utf-8').strip()
		except IOError:
			return ''
