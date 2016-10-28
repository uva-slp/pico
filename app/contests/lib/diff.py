"""
author: Nathan Williams
created: 10/18/2016

diff.py is concerned with the comparison of two string lists
"""

import difflib
import re
from .html import Table, Row, Th, Td, Div, Span, Mark

"""
Generates HTML containing the diff of two string lists
"""
class HtmlFormatter():
	def __init__(self, fromlines, tolines, emptylines=True, whitespace=True, distinguish_changed=False):
		self.fromlines = fromlines
		self.tolines = tolines
		self.emptylines = emptylines
		self.whitespace = whitespace
		self.distinguish_changed = distinguish_changed

	def asTable(self):
		table = Table().addClass('diff-table')
		
		headers = Row()
		headers.addCell(Th('Submission', 2))
		headers.addCell(Th('Solution', 2))
		table.addHeader(headers)

		num_changes = 0
		for diff in difflib._mdiff(self.fromlines, self.tolines):
			fromline, toline, hasChange = self.clean(diff)
			row = Row()

			# tag
			tag = ''
			if hasChange:
				tag = str(Span().setElementId(num_changes))
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
			row.addCell(Td(Div(line_num))
				.addClass('diff-cell')
				.addClass('line-number'))
			row.addCell(Td(self.prepare(1, text))
				.addClass('diff-cell')
				.addClass('line-text'))

			table.addRow(row)

		return str(table), num_changes

	"""
	Filters deltas to exclude whitespace and blank lines based on empty_lines and whitespace.
	"""
	def clean(self, diff):
		fromLine, toLine, hasChange = diff
		if not hasChange:
			return fromLine, toLine, hasChange

		fromLine, hasChange = self.clean_line(0, fromLine, toLine[0]=='')
		toLine, hasChange = self.clean_line(1, toLine, fromLine[0]=='', hasChange)

		return fromLine, toLine, hasChange

	"""
	Helper for #clean.
	"""
	def clean_line(self, side, line, solo, hasChange=False):
		line_num, text = line
		marker = '-' if side == 0 else '+'

		if not self.emptylines:
			text = re.sub('^(\s*)(\0\+|\0\-|\0\^)(\s*)\1(\s*)$', lambda m: m.group(1)+m.group(3)+m.group(4), text)
		if not self.whitespace:
			text = re.sub('(\0\+|\0\-|\0\^)(.*)(\1)', self.unmark_whitespace, text)
		if self.emptylines and solo and text.isspace():
			text = '\0%s \1'%(marker)

		return (line_num, text), (hasChange or '\x00' in text)

	"""
	Replace function for whitespace filtering in #clean_line
	"""
	def unmark_whitespace(self, matchgrp):
		open_tag, content, close_tag = matchgrp.groups()
		if content.isspace():
			return content

		content = re.sub('(?<=[^\s])(\s+)|(\s+)(?=[^\s])', lambda m: close_tag+(m.group(1) or m.group(2))+open_tag, content)
		return open_tag + content + close_tag

	"""
	Wraps text indicated by difflib (surrounded with \x00 and \x01) with a span and assigns the appropriate classes so that additions are highlighted green and deletions are highlighted red
	"""
	def prepare(self, side, text):
		div = Div()
		span = Span().addClass('diff-text')
		change = None
		
		i = 0
		while i < len(text):
			if text[i] == '\x00':
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
				right = text.find('\x01', left)
				
				for ch in text[left:right]:
					span.append(Span(ch).addClass(spanClass))

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
