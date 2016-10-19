"""
author: Nathan Williams
created: 10/18/2016

diff.py is concerned with the comparison of two string lists
"""

import difflib
from html import Table, Row, Th, Td, Div, Span, Mark

"""
Generates HTML containing the diff of two string lists
"""
class HtmlFormatter():
	def __init__(self, fromlines, tolines):
		self.fromlines = fromlines
		self.tolines = tolines

	def asTable(self):
		table = Table().addClass('diff-table')
		
		headers = Row()
		headers.addCell(Th('Submission', 2))
		headers.addCell(Th('Solution', 2))
		table.addHeader(headers)

		numChanges = 0 # number of changes
		diff = list(difflib._mdiff(self.fromlines, self.tolines))
		for fromLine, toLine, hasChange in diff:
			row = Row()

			# tag
			tag = ''
			if hasChange:
				tag = str(Span().setElementId(numChanges))
				numChanges+=1

			# from
			lineNo, text = fromLine
			row.addCell(Td(Div(tag+str(lineNo)))
				.addClass('diff-cell')
				.addClass('line-number'))
			row.addCell(Td(prepare(text))
				.addClass('diff-cell')
				.addClass('line-text'))

			# to
			lineNo, text = toLine
			row.addCell(Td(Div(lineNo))
				.addClass('diff-cell')
				.addClass('line-number'))
			row.addCell(Td(prepare(text))
				.addClass('diff-cell')
				.addClass('line-text'))

			table.addRow(row)

		return str(table), numChanges

"""
Wraps text indicated by difflib (surrounded with \x00 and \x01) with a span and assigns the appropriate classes so that additions are highlighted green and deletions are highlighted red
"""
def prepare(text):
	div = Div()
	change = None
	
	i = 0
	while i < len(text):
		if text[i] == '\x00':
			change = text[i+1]
			if change == '+':
				spanClass = 'added'
			else: # change == '-'
				spanClass = 'deleted'
			
			left = i+2
			right = text.find('\x01', left)
			
			for ch in text[left:right]:
				div.append(Span(ch).addClass(spanClass))

			i = right
		
		else:
			div.append(text[i])
		i+=1

	if change:
		if change == '+':
			div.addClass('added-bg')
		else: # text[i] == '-'
			div.addClass('deleted-bg')

	return str(div)
