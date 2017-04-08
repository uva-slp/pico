"""
author: Nathan Williams
created: 10/18/2016

diff.py is concerned with the comparison of two string lists
"""

import difflib
import re
from .html import Table, Row, Th, Td, Div, Span, Anchor

"""
Generates HTML containing the diff of two string lists
"""
class HtmlFormatter():
	def __init__(self, fromlines=None, tolines=None, emptylines=True, whitespace=True, distinguish_changed=False):
		self.fromlines = fromlines
		self.tolines = tolines
		self.emptylines = emptylines
		self.whitespace = whitespace
		self.distinguish_changed = distinguish_changed

	def asTable(self):
		table = Table().addClass('diff-table')
		
		headers = Row().addCell(Th()).addCell(Th('Submission'))
		headers.addCell(Th()).addCell(Th('Solution'))
		table.addHeader(headers)

		num_changes = 0
		for diff in difflib._mdiff(self.fromlines, self.tolines):
			fromline, toline, hasChange = diff
			row = Row()

			# tag
			tag = ''
			if hasChange:
				tag = str(Anchor().setName(num_changes))
				num_changes+=1

			# from
			line_num, text = fromline
			line_num = line_num if len(str(line_num)) > 0 else '&nbsp;'
			row.addCell(Td(Div(tag+str(line_num)))
				.addClass('diff-cell')
				.addClass('line-number'))
			row.addCell(Td(self.prepare(0, text))
				.addClass('diff-cell')
				.addClass('line-text'))

			# to
			line_num, text = toline
			line_num = line_num if len(str(line_num)) > 0 else '&nbsp;'
			row.addCell(Td(Div(line_num))
				.addClass('diff-cell')
				.addClass('line-number'))
			row.addCell(Td(self.prepare(1, text))
				.addClass('diff-cell')
				.addClass('line-text'))

			table.addRow(row)

		return str(table), num_changes

	"""
	Wraps text indicated by difflib (surrounded with \0 and \1) with a span and assigns the appropriate classes so that additions are highlighted green and deletions are highlighted red
	"""
	def prepare(self, side, text):
		div = Div().addClass('diff-text')
		span = Span()
		change = None
		emptyline = re.compile('^(\s*)(\0\+|\0\-|\0\^)(\s*)\1(\s*)$').match(text) is not None
		
		i = 0
		while i < len(text):
			if text[i] == '\0':
				change = text[i+1]
				if change == '+':
					spanClass = 'diff-add'
				elif change == '-':
					spanClass = 'diff-del'
				elif change == '^':
					if self.distinguish_changed:
						spanClass = 'diff-chg'
					elif side == 0:
						spanClass = 'diff-del'
					else:
						spanClass = 'diff-add'
				
				left = i+2
				right = text.find('\1', left)

				for s in re.split(r'(\s+)', text[left:right]):
					if not s: continue
					s_span = Span(s).addClass(spanClass)
					if s.isspace() and not emptyline:
						s_span.addClass('diff-whitespace')
					if emptyline:
						s_span.addClass('diff-emptyline')
					span.append(s_span)

				i = right
			
			else:
				span.append(text[i])
			i+=1
		
		div.append(span)

		if change:
			if change == '+':
				div.addClass('diff-add-bg')
			elif change == '-':
				div.addClass('diff-del-bg')
			elif change == '^':
				if self.distinguish_changed:
					div.addClass('diff-chg-bg')
				elif side == 0:
					div.addClass('diff-del-bg')
				else:
					div.addClass('diff-add-bg')

		return div
