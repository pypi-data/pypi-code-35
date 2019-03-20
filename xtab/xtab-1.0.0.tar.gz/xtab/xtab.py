#! /usr/bin/python
"""xtab.py

PURPOSE
   Read a table (from a text file) of data in normalized form and cross-tab it,
   allowing multiple data columns to be crosstabbed.

AUTHOR
	R. Dreas Nielsen (RDN)

COPYRIGHT AND LICENSE
	Copyright (c) 2007-2018, R.Dreas Nielsen
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.
	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.
	The GNU General Public License is available at <http://www.gnu.org/licenses/>

NOTES
	1. This code can be used either as a module or as a stand-alone script.
	2. The sole function intended to be used by callers of this module is 'xtab()'.
	3. When there are multiple values in the input that should go into a single
		cell of the output, only the first of these is written into that cell
		('first' is indeterminate).  The 'xtab()' function allows logging of
		the data selection statement (SQL) used to obtain the data for each cell,
		and the result(s) obtained, and thus to determine which cell(s) have
		multiple values.
=====================================================================================
"""

#=====================================================================================
# TODO:
#	* Implement a class to wrap csv reader and writer objects
#	  to ensure appropriate closure of underlying file objects
#	  on error.  (Or use 'with' in 2.6/3.0)
#	* Implement error-checking of the column names in the command
#	  line arguments prior to calling 'xtab()'.
#	* Add more specific error traps throughout.
#=====================================================================================


_version = "1.0.0"
_vdate = "2019-03-19"

import sys
import os
import os.path
import csv
import sqlite3
import copy
import logging
import traceback

_errmsg_noinfile = "No input filename specified."
_errmsg_badinfile = "Input file does not exist."
_errmsg_nooutfile = "No output filename specified."
_errmsg_norowheaders = "No row header columns specified."
_errmsg_nocolumheaders = "No column header columns specified."
_errmsg_nocellcolumns = "No cell value columns specified."
_errmsg_baderrlogfile = "Only one error log file name should be specified."
_errmsg_badsqllogfile = "Only one SQL log file name should be specified."

__help_msg = """Required Arguments:
   -i <filename>
      The name of the input file from which to read data.
      This must be a text file, with data in a normalized format.
      The first line of the file must contain column names.
   -o <filename>
      The name of the output file to create.
      The output file will be created as a .csv file.
   -r <column_name1> [column_name2 [...]]
      One or more column names to use as row headers.
      Unique values of these columns will appear at the beginning of every
      output line.
   -c <column_name1> [column_name2 [...]]
      One or more column names to use as column headers in the output.
      A crosstab column (or columns) will be created for every unique
      combination of values of these fields in the input.
   -v <column_name1> [column_name2 [...]]
      One or more column names with values to be used to fill the cells
      of the cross-table.  If n columns names are specified, then there will
      be n columns in the output table for each of the column headers
      corresponding to values of the -c argument.  The column names specified
      with the -v argument will be appended to the output column headers
      created from values of the -c argument.  There should be only one value
      of the -v column(s) for each combination of the -r and -c columns;
      if there is more than one, a warning will be printed and only the first
      value will appear in the output.  (That is, values are not combined in
      any way when there are multiple values for each output cell.)
Optional Arguments:
   -d[1|2|3|4]
      Controls the format of column headers.  The four alternatives are:
      -d1 or no option specified
         One row of column headers, with elements joined by underscores
         to facilitate parsing by other programs.
      -d or -d2
         Two rows of column headers.  The first row contains values of the
         columns specified by the -c argument, and the second row contains
         the column names specified by the -v argument.
      -d3
         One header row for each of the values of the columns specified by
         the -c argument, plus one row with the column names specified by
         the -v argument.
      -d4
         Like -d3, but the values of the columns specified by the -c
         argument are labeled with (preceded by) the column names.
   -f
      Use a temporary (sqlite) file instead of memory for intermediate
      storage.
   -k
      Keep (i.e., do not delete) the sqlite file.  Only useful with the
      "-f" option.  Unless the "-t" option is also used, the table name will
      be "src".
   -n <default_string>
      Use the specified default string in the output wherever an empty or
	  null value would otherwise appear.
   -s Sort columns and rows in ascending alphabetic order.
   -t <tablename>
      Name to use for the table in the intermediate sqlite database.  Only
      useful with the "-f" and "-k" options.
   -e [filename]
      Log all error messages, to a file if the filename is specified or to the
      console if the filename is not specified.
   -q <filename>
      Log the sequence of SQL commands used to extract data from the input
      file to write the output file, including the result of each command.
   -h
      Print this help and exit.
Notes:
   1. Column names should be specified in the same case as they appear in the
      input file.
   2. The -f option creates a temporary file in the same directory as the
      output file.  This file has the same name as the input file, but an
      extension of '.sqlite'.
   3. There are no inherent limits to the number of rows or columns in the
      input or output files.
   4. Missing required arguments will result in an exception rather than an
      error message, whatever the error logging option.  If no error logging
      option is specified, then if there are multiple values per cell (the
      most likely data error), a single message will be printed on the console.
"""

# enum for header row codes
hdrs_1, hdrs_2, hdrs_many, hdrs_labeled = (1, 2, 3, 4)

def xtab(infilename, rownames, xtab_colnames, xtab_datanames, outfilename,
		 header_rows=hdrs_1, file_db=False, keep_file_db=False, tablename="src",
		 error_reporter=None, sql_reporter=None, nullfill=None, sort_alpha=False):
	"""Cross-tab data in the specified input file and write it to the output file.
	Arguments:
		infilename: string of the input file name.  Some diagnosis of file format
			(CSV or tab formatted) will be performed.
		rownames: list of strings of column names in the input file that will be used
			as row headers in the output file.
		xtab_colnames: list of strings of column names in the input file that will be
			used as primary column headers in the output file.
		xtab_datanames: list of strings of column names in the input file that will be
			crosstabbed in the output file.  These column names will also be used as
			secondary column names in the output file.
		outfilename: string of the output file name.  This file will all be written as CSV.
		dualheader: boolean controlling whether or not there will be one or two header
			rows in the output file.  If a single header row is used, then the primary and
			secondary column headers will be joined in each column header.  If two column
			headers are used, then the primary column headers will be used on the first
			line of headers, and the secondary column headers will be used on the second
			line of headers.
		file_db: boolean controlling whether or not the sqlite db is created as a disk file
			(if True) or in memory (if False, the default).
		keep_file_db: boolean controlling whether or not a sqlite disk file is retained
			(if True) or deleted after it has been used.
		error_reporter: logging.Logger object to report nonfatal errors (specifically, the presence
			of more than one value for a cell).
		sql_reporter: logging.Logger object to report the sqlite queries executed and their
			results.
		nullfill: the value with which to replace null (empty) values in the output.
	Return value
		The number of warnings or errors encountere.

	When multiple column headers in the input file are used as a single column header in
	the output file, the column names are joined with an underscore.  This is to facilitate
	any subsequent parsing to be done by other programs (e.g., R).
	"""
	multiple_vals = False		# A flag indicating whether or not multiple values were found for a single crosstab cell
	if sys.version_info < (3,0,0):
		outfile = open(outfilename, "wb")	# The Py2 csv module adds an extra <CR> if "wt" is specified
	else:
		outfile = open(outfilename, "w")
	csvout = csv.writer(outfile)
	reportable_errors = 0
	
	# Move the data into sqlite for easy random access.
	if file_db:
		inhead, intail = os.path.split(infilename)
		sqldbname = os.path.join(inhead, os.path.splitext(intail)[0] + ".sqlite")
		try:
			os.unlink(sqldbname)
		except:
			pass
	else:
		sqldbname = None
	if tablename == None:
		tablename = "src"
	sqldb = copy_to_sqlite(infilename, sqldbname, tablename)

	# Get list of unique values for 'xtab_colnames' columns
	if sort_alpha:
		sqlcmd = "select distinct %s from %s order by %s;" % (",".join(xtab_colnames), tablename, ",".join(xtab_colnames))
	else:
		sqlcmd = "select distinct %s from %s;" % (",".join(xtab_colnames), tablename)
	xtab_vals = sqldb.execute(sqlcmd).fetchall()

	# Write output headers.
	if header_rows == hdrs_1:
		# One header row
		outstrings = [n for n in rownames]
		for n in xtab_vals:
			for i in xtab_datanames:
				outstrings.append("%s_%s" % ("_".join(n), i.replace("'", "''")))
		csvout.writerow(outstrings)
	elif header_rows == hdrs_2:
		# Two header rows
		extra_cols = len(xtab_datanames) - 1
		# Write header row 1/2
		outstrings = ['' for n in rownames]
		for n in xtab_vals:
			hdr = " ".join(n)
			outstrings.append(hdr.replace("'", "''"))
			for i in range(extra_cols):
				outstrings.append('')
		csvout.writerow(outstrings)
		# Write header row 2/2
		outstrings = [n for n in rownames]
		for n in xtab_vals:
			for i in xtab_datanames:
				outstrings.append(i.replace("'", "''"))
		csvout.writerow(outstrings)
	elif header_rows == hdrs_many:
		# One header row for each item in xtab_vals plus a row
		# for xtab_datanames.
		extra_cols = len(xtab_datanames) - 1
		for i in range(len(xtab_colnames)):
			outstrings = ['' for n in rownames]
			for n in xtab_vals:
				outstrings.append(n[i].replace("'", "''"))
				for x in range(extra_cols):
					outstrings.append('')
			csvout.writerow(outstrings)
		# Write last header row of xtab_datanames
		outstrings = [n for n in rownames]
		for n in xtab_vals:
			for i in xtab_datanames:
				outstrings.append(i.replace("'", "''"))
		csvout.writerow(outstrings)
	else:	# header_rows == hdrs_labeled
		extra_cols = len(xtab_datanames) - 1
		for i in range(len(xtab_colnames)):
			outstrings = ['' for n in rownames]
			for n in xtab_vals:
				outstrings.append("%s: %s" % (xtab_colnames[i], n[i].replace("'", "''")))
				for x in range(extra_cols):
					outstrings.append('')
			csvout.writerow(outstrings)
		# Write last header row of xtab_datanames
		outstrings = [n for n in rownames]
		for n in xtab_vals:
			for i in xtab_datanames:
				outstrings.append(i.replace("'", "''"))
		csvout.writerow(outstrings)

	# Write output data
	# For each unique combination of row headers
	#	Initiate a new output line
	#	Get the row headers
	#		For every item in the xtab_vals
	#			Select the 'xtab_datanames' columns from sqlite for the row headers and xtab_vals
	#			Append the first result (set warning if >1) to the output line
	#	Write the output line
	#
	# Get a list of unique combinations of row headers
	if sort_alpha:
		sqlcmd = "SELECT DISTINCT %s FROM %s ORDER BY %s;" % (",".join(rownames), tablename, ",".join(rownames))
	else:
		sqlcmd = "SELECT DISTINCT %s FROM %s;" % (",".join(rownames), tablename)
	row_hdr_vals = sqldb.execute(sqlcmd).fetchall()
	row_counter = 0

	for l in row_hdr_vals:
		row_counter = row_counter + 1
		col_counter = 0
		outstrings = []
		# Add the row headers to the list of outstrings
		for rn in range(len(l)):
			outstrings.append(l[rn].replace("'", "''"))
		# Make a list of WHERE conditions for the row header variables
		sqlcond = ["%s='%s'" % (rownames[i], l[i].replace("'", "''")) for i in range(len(rownames))]
		for n in xtab_vals:
			col_counter = col_counter + 1
			# Add the WHERE conditions for the crosstab values
			selcond = copy.deepcopy(sqlcond)
			for cn in range(len(xtab_colnames)):
				selcond.append("%s='%s'" % (xtab_colnames[cn], n[cn].replace("'", "''")))
			# Create and execute the SQL to get the data values
			sqlcmd = "SELECT %s FROM %s WHERE %s" % (",".join(xtab_datanames), tablename, " AND ".join(selcond))
			if sql_reporter:
				sql_reporter.log(logging.INFO, "%s" % sqlcmd)
			data_vals = sqldb.execute(sqlcmd).fetchall()
			if sql_reporter:
				for r in data_vals:
					sql_reporter.log(logging.INFO, "\t%s" % "\t".join(r))
			if len(data_vals) > 1:
				multiple_vals = True
				reportable_errors += 1
				if error_reporter:
					error_reporter.log(logging.WARNING, "Multiple result rows for the command '%s'--only the first is used." % (sqlcmd))
			if len(data_vals) == 0:
				if nullfill:
					for n in range(len(xtab_datanames)):
						outstrings.append(nullfill)
				else:
					for n in range(len(xtab_datanames)):
						outstrings.append('')
			else:
				data = data_vals[0]
				for n in range(len(xtab_datanames)):
					outstrings.append(data[n])
		csvout.writerow(outstrings)
	sqldb.close()
	if file_db and not keep_file_db:
		try:
			os.unlink(sqldbname)
		except:
			pass
	outfile.close()
	if multiple_vals and not error_reporter:
		msg = "Warning: multiple data values found for at least one crosstab cell; only the first is displayed."
		print(msg)
		if error_reporter:
			error_reporter(msg)
	return reportable_errors


def unquote(str):
	"""Remove quotes surrounding a string."""
	if len(str) < 2:
		return str
	c1 = str[0]
	c2 = str[-1:]
	if c1==c2 and (c1=='"' or c1=="'"):
		return str[1:-1].replace("%s%s" % (c1, c1), c1)
	return str


def quote_str(str):
	"""Add single quotes around a string."""
	if len(str) == 0:
		return "''"
	if len(str) == 1:
		if str == "'":
			return "''''"
		else:
			return "'%s'" % str
	if str[0] != "'" or str[-1:] != "'":
		return "'%s'" % str.replace("'", "''")
	return str


def quote_list(l):
	"""Add single quotes around all strings in the list."""
	return [quote_str(x) for x in l]


def quote_list_as_str(l):
	"""Convert a list of strings to a single string of comma-delimited, quoted tokens."""
	return ",".join(quote_list(l))


def del_file(fn):
	"""Deletes the specified file if it exists."""
	if os.path.isfile(fn):
		os.unlink(fn)


def copy_to_sqlite(data_fn, sqlite_fn=None, tablename="src"):
	"""Copies data from a CSV file to a sqlite table.
	Arguments:
		data_fn: a string of the data file name with the data to be read.
		sqlite_fn: a string of the name of the sqlite file to create, or None if 
			sqlite is to use memory instead.
		tablename: the name of the sqlite table to create
	Value:
		The sqlite connection object.
	"""
	dialect = csv.Sniffer().sniff(open(data_fn, "rt").readline())
	inf = csv.reader(open(data_fn, "rt"), dialect)
	column_names = next(inf)
	if sqlite_fn == None:
		conn = sqlite3.connect(":memory:")
	else:
		try:
			os.unlink(sqlite_fn)
		except:
			pass
		conn = sqlite3.connect(sqlite_fn)
	if tablename == None:
		tablename = "src"
	colstr = ",".join(column_names)
	try:
		conn.execute("drop table %s;" % tablename)
	except:
		pass
	conn.execute("create table %s (%s);" % (tablename, colstr))
	for l in inf:
		sql = "insert into %s values (%s);" % (tablename, quote_list_as_str(l))
		conn.execute(sql)
		conn.commit()
	return conn


def print_help():
	"""Print a program description and brief usage instructions to the console."""
	print("xtab %s %s -- Cross-tabulates data." % (_version, _vdate))
	print(__help_msg)

	
def get_opts(arglist):
	"""Returns a dictionary of command-line arguments.  This custom 'getopt' routine is used
	to allow multiple column names for the -r, -c, and -v arguments with only one use of each
	flag.
	"""
	argdict = {}
	nargs = len(arglist)
	argno = 1
	currarg = None
	currargitems = []
	while argno < nargs:
		arg = arglist[argno]
		if len(arg) > 0:
			if arg[0] == '-':
				if currarg:
					argdict[currarg] = currargitems
				currarg = arg
				currargitems = []
			else:
				if currarg:
					currargitems.append(arg)
				else:
					argdict[arg] = []
		argno += 1
	if currarg:
		argdict[currarg] = currargitems
	return argdict


def main():
	"""Read and interpret the command-line arguments and options, and carry out
	the appropriate actions."""
	args = get_opts(sys.argv)
	if len(args) == 0 or '-h' in args or '--help' in args:
		print_help()
		sys.exit(0)
	badopts = [ o for o in args.keys() if o not in ['-i', '-o', '-r',
		'-c', '-v', '-d', '-d1', '-d2', '-d3', '-d4', '-f', '-k', '-s', '-t',
		'-n', '-e', '-q'] ]
	if len(badopts) > 0:
		raise ValueError("Unrecognized option(s): %s" % ", ".join(badopts))
	if '-i' in args:
		if len(args['-i']) == 0:
			raise ValueError(_errmsg_noinfile)
		infilename = args['-i'][0]
		if not os.path.exists(infilename):
			raise ValueError("%s (%s)" % (_errmsg_badinfile, infilename))
	else:
		raise ValueError(_errmsg_noinfile)
	#
	if '-o' in args:
		if len(args['-o']) == 0:
			raise ValueError(_errmsg_nooutfile)
		outfilename = args['-o'][0]
	else:
		raise ValueError(_errmsg_nooutfile)
	#
	if '-r' in args:
		if len(args['-r']) == 0:
			raise ValueError(_errmsg_norowheaders)
		rowheaders = args['-r']
	else:
		raise ValueError(_errmsg_norowheaders)
	#
	if '-c' in args:
		if len(args['-c']) == 0:
			raise ValueError(_errmsg_nocolumheaders)
		columnheaders = args['-c']
	else:
		raise ValueError(_errmsg_nocolumheaders)
	#
	if '-v' in args:
		if len(args['-v']) == 0:
			raise ValueError(_errmsg_nocellcolumns)
		cellvalues = args['-v']
	else:
		raise ValueError(_errmsg_nocellcolumns)
	#
	hdr_opt = hdrs_1
	if '-d' in args or '-d2' in args:
		hdr_opt = hdrs_2
	if '-d3' in args:
		hdr_opt = hdrs_many
	if '-d4' in args:
		hdr_opt = hdrs_labeled
	file_db = '-f' in args
	keep_file_db = '-k' in args
	tablename = 'src'
	if '-t' in args:
		if len(args['-t']) == 1:
			tablename = args['-t'][0]
	nullfill = None
	if '-n' in args:
		if len(args['-n']) == 1:
			nullfill = args['-n'][0]
	sort_alpha = '-s' in args
	#
	# Set up logging
	#logging.basicConfig(level=logging.INFO, filemode="w", filename='')
	err_logger = None
	sql_logger = None
	error_file = None
	if '-e' in args:
		err_logger = logging.getLogger("err")
		err_logger.setLevel(logging.WARNING)
		if len(args['-e']) == 0:
			err_logger.addHandler(logging.StreamHandler())
		else:
			if len(args['-e']) > 1:
				raise ValueError(_errmsg_baderrlogfile)
			error_file = args['-e'][0]
			del_file(error_file)
			file_logger = logging.FileHandler(error_file, "w")
			err_logger.addHandler(file_logger)
	if '-q' in args:
		if len(args['-q']) != 1:
			raise ValueError(_errmsg_badsqllogfile)
		sql_logger = logging.getLogger("sql")
		sql_logger.setLevel(logging.INFO)
		sql_logger.addHandler(logging.FileHandler(args['-q'][0], "w"))
	#
	errors = xtab(infilename, rowheaders, columnheaders, cellvalues, outfilename, hdr_opt,
	 file_db, keep_file_db, tablename, err_logger, sql_logger, nullfill, sort_alpha)
	if errors == 0 and error_file is not None:
		# Logger can create the file if a message below the warning level
		# is issued, even though it will not be logged.
		file_logger.close()
		del_file(error_file)



if __name__=='__main__':
	try:
		main()
	except SystemExit as x:
		sys.exit(x)
	except ValueError as e:
		sys.stderr.write("%s\n" % str(e))
		sys.exit(1)
	except Exception:
		strace = traceback.extract_tb(sys.exc_info()[2])[-1:]
		lno = strace[0][1]
		src = strace[0][3]
		sys.stderr.write("%s: Uncaught exception %s (%s) on line %s (%s)." % (os.path.basename(sys.argv[0]), str(sys.exc_info()[0]), sys.exc_info()[1], lno, src))
		sys.exit(1)

