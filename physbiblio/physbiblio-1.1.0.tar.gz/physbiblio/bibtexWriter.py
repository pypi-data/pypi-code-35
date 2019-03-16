"""Module that contains the PBBibTexWriter class
(needed to override _entry_to_bibtex).

This file is part of the physbiblio package.
"""
from bibtexparser.bwriter import BibTexWriter


class PBBibTexWriter(BibTexWriter):
	"""This class is used to override _entry_to_bibtex"""

	def __init__(self):
		"""Constructor for the PBBibTexWriter class.
		Uses parent class constructor
		and adds some additional properties.
		"""
		super(PBBibTexWriter, self).__init__()
		#use 13 characters for the field name:
		self._max_field_width = 13
		#order of fields in output
		self.display_order = [
			'author', 'collaboration', 'title', 'booktitle', 'publisher',
			'journal', 'volume', 'year', 'pages',
			'russian',
			'archiveprefix', 'primaryclass', 'eprint', 'doi',
			'reportNumber']
		self.bracket_fields = ['title', 'booktitle', 'www', 'note',
			'abstract', 'comment', 'article', 'url']
		self.excluded_fields = ["adsnote", "adsurl", "slaccitation"]
		#Necessary to avoid a change of the ordering of the bibtex entries:
		self.order_entries_by = None
		self.comma_first = False

	def _entry_to_bibtex(self, entry):
		"""Redefine the function that writes
		the entries in the bib file.
		Adapted from
		`bibtexparser.bwriter.BibTexWriter._entry_to_bibtex`.

		Parameters:
			entry: a dictionary generated by bibtexparser.

		Output:
			the bibtex string
		"""
		bibtex = ''
		# Write BibTeX key
		bibtex += '@' + entry['ENTRYTYPE'].capitalize() + '{' \
			+ ( entry['ID'] if entry['ID'] is not None else "" )

		# create display_order of fields for this entry
		# first those keys which are both
		# in self.display_order and in entry.keys
		display_order = [i for i in self.display_order if i in entry]
		# then all the other fields sorted alphabetically
		display_order += [i for i in sorted(entry) \
			if i not in self.display_order and i not in self.excluded_fields]

		# Write field = value lines
		for field in [i for i in display_order if i not in ['ENTRYTYPE', 'ID']]:
			try:
				entry[field] = entry[field].replace("{{{", "{").replace(
					"}}}", "}")
				bibtex += ",\n" + self.indent + "{0:>{1}}".format(
					field, self._max_field_width) + ' = "' \
					+ ("{"+entry[field]+"}" \
						if field in self.bracket_fields and \
							(entry[field][0] != "{" \
							or entry[field][-1] != "}") \
						else entry[field]) + '"'
			except TypeError:
				raise TypeError(u"The field %s in entry %s must be a string"
								% (field, entry['ID']))
		bibtex += ",\n}\n" + self.entry_separator
		return bibtex


pbWriter = PBBibTexWriter()
