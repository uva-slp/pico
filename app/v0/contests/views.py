from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from difflib import HtmlDiff # temporary

from lib import diff as _diff

def home(request):
	j = "foo"
	foo = "Make Travis run"
	please="please"
	please == please
	return HttpResponse('home page %s'%(please+foo+j))

def diff(request):
	fromlines = ['foo', 'bar', 'flarp']
	tolines = ['food', 'jip', 'bar', 'zoo', 'jaslkdfj;laskdjflasdlkflasdgflkjghkljcvkljadkjlfhkajsldfhlkawheuifyiasdhflkjashdjklfhkajsdhflkjashiudfyoiauwhelkfjhaslkjdfhklasjhdfkljashdkflj']

	html, numChanges = _diff.HtmlFormatter(fromlines, tolines).asTable()

	return render(
		request,
		'contests/diff.html',
		{'diff_table': html, 'numChanges': numChanges})
