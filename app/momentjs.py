from jinja2 import Markup

class momentjs(object):
	"""" Moment JS Wrapper
		We are using Moment JS TO render dates and times according to the client configured locale.
	"""

	def __init__(self, timestamp):
		self.timestamp = timestamp

	def render(self, format):
		# markup is for do not scape string
		return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))

	def format(self, fmt):
		return self.render("format(\"%s\")" % frm)

	def calendar(self):
		return self.render("calendar()")

	def fromNow(self):
		return self.render("fromNow()")

