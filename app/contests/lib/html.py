"""
author: Nathan Williams
created: 10/18/2016

html.py encapsulates key DOM elements and generates valid HTML given the contents of those elements
"""

class Element():
	def __init__(self, tag, content=''):
		self.tag = str(tag)
		self.elid = ''
		self.name = ''
		self.classes = []
		self.style = {}
		self.properties = {}
		self.content = str(content)

	def __str__(self):
		return '<{0}{1}{2}{3}{4}{5}>{6}</{0}>'.format(
			self.tag,
			' id="%s"'%(self.elid) if self.elid else '',
			' name="%s"'%(self.name) if self.name else '',
			' class="%s"'%(self.classesStr()) if self.classes else '',
			' style="%s"'%(self.styleStr()) if self.style else '',
			' %s'%(self.propertiesStr()) if self.properties else '',
			self.innerHtml())

	def setElementId(self, elid):
		self.elid = str(elid)
		return self

	def setName(self, name):
		self.name = str(name)
		return self

	def classesStr(self):
		return ' '.join(self.classes)

	def addClass(self, c):
		self.classes.append(c)
		return self

	def styleStr(self):
		return ';'.join('{0}:{1}'.format(str(k),str(v)) for k,v in self.style.items())
	
	def addStyle(self, key, value):
		self.style[key] = value
		return self

	def propertiesStr(self):
		return ' '.join(['{0}="{1}"'.format(str(k),str(v)) for k,v in self.properties.items()])

	def addProperty(self, key, value):
		self.properties[key] = value
		return self

	def innerHtml(self):
		return self.content

	def append(self, s):
		self.content += str(s)
		return self

class Table(Element):
	def __init__(self):
		super().__init__('table')
		self.headers = []
		self.rows = []

	def innerHtml(self):
		thead = ''.join(str(header) for header in self.headers)
		tbody = ''.join(str(row) for row in self.rows)
		return  '<thead>{0}</thead><tbody>{1}</tbody>'.format(thead, tbody)

	def addHeader(self, header):
		self.headers.append(header)

	def addRow(self, row):
		self.rows.append(row)

class Row(Element):
	def __init__(self):
		super().__init__('tr')
		self.cells = []

	def innerHtml(self):
		return ''.join(str(cell) for cell in self.cells)

	def addCell(self, cell):
		self.cells.append(cell)

class Th(Element):
	def __init__(self, content='', colSpan=1):
		super().__init__('th', content)
		self.addProperty('colSpan', colSpan)

class Td(Element):
	def __init__(self, data=''):
		super().__init__('td', data)

class Div(Element):
	def __init__(self, content=''):
		super().__init__('div', content)

class Span(Element):
	def __init__(self, content=''):
		super().__init__('span', content)

class Mark(Element):
	def __init__(self, content=''):
		super().__init__('mark', content)

class Anchor(Element):
	def __init__(self, content=''):
		super().__init__('a', content)
