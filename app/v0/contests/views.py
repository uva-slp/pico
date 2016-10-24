from django.shortcuts import render, redirect

from teams.forms import TeamForm, TeamJoinForm, TeamLeaveForm
from lib import diff as _diff

def home(request):
	return render(
		request,
		'contests/home.html',
		{'team_form': TeamForm(), 'team_join_form': TeamJoinForm(request), 'team_leave_form': TeamLeaveForm(request)})

def diff(request):
	fromlines = ['foo', 'bar', 'flarp']
	tolines = ['food', 'jip', 'bar', 'zoo', 'jaslkdfj;laskdjflasdlkflasdgflkjghkljcvkljadkjlfhkajsldfhlkawheuifyiasdhflkjashdjklfhkajsdhflkjashiudfyoiauwhelkfjhaslkjdfhklasjhdfkljashdkflj']

	html, numChanges = _diff.HtmlFormatter(fromlines, tolines).asTable()

	return render(
		request,
		'contests/diff.html',
		{'diff_table': html, 'numChanges': numChanges})
