"""
 Project: root_report                                                           
    File: $Id: Report.py
 Authors:                                                                  
   Lucio Anderlini, Istituto Nazionale di Fisica Nucleare - Sezione di Firenze
                                                                           
 Copyright (c) 2019 - CERN on behalf of the LHCb Collaboration 
                                                                           
 Redistribution and use in source and binary forms,                        
 with or without modification, are permitted according to the terms        
 listed in LICENSE (https://root.cern.ch/license)             
"""
from __future__ import print_function 

from ROOT import gPad, TCanvas
import datetime
import os


class Report:
  def __init__( self
                , filename
                , path = './www/'
                , options = ''
                , enabled = True
              ):
    """
    Constructor for Report class.

    Arguments:
     . filename, name of the output file report
     . path, direcotory where the file is saved
     . options (string):
        > saveMacro
    """
    self._filename       = filename
    self._path           = path
    self._options        = options
    self._figIndex       = 0
    self._enabled        = enabled

    self._myCanvas = TCanvas(filename, filename, int(1.618033*600), 600)
    self._myCanvas.SetLeftMargin   (0.16) 
    self._myCanvas.SetRightMargin  (0.05) 
    self._myCanvas.SetTopMargin    (0.05) 
    self._myCanvas.SetBottomMargin (0.20) 

    self._myCanvas.cd()

    if not self._enabled: return
    
    self._file = open(path+'/'+filename+".html", 'w')
    self._file.write("""
      <HTML>
        <HEAD>
          <TITLE>"""+filename+"""</TITLE>
        </HEAD>
        <BODY>
    """)

  def timestamp (self, html="%s", forma="{:%Y-%m-%d %H:%M:%S}"):
    if not self._enabled: return
    forma = forma.format(datetime.datetime.now())
    self._file.write(str(html%(forma,)))
    return self

  def outputTable ( self , rowList, opt ):
    if not self._enabled: return

    self._file.write( "<TABLE %s>" % (opt,)  )
    for row in rowList:
      self._row ( row )
    self._file.write( "</TABLE>" )
    return self
  
  def _row ( self, columns ):
    if not self._enabled: return
    self._file.write ( "<TR>" )
    for column in columns:
      self._file.write ( "<TD>" )
      self._file.write ( str(column) )
    self._file.write ( "</TR>" )
    

  def __lshift__(self, text):
    if not self._enabled: return
    self._file.write(str(text))
    return self

  def outputTitle(self, title):
    if not self._enabled: return
    self._file.write("<H1>"+title+"</H1>")


  def _figureFileName(self, name, extension):
    if not self._enabled: return
    return "img/Fig-" + self._filename + "_"  \
            + str(self._figIndex) + "_" + name + "." + extension

  def outputCanvas(self, name, options="width=45%", thumb_fmt='png', vector_fmt='pdf'):
    "Saves the current Canvas to pdf and png files, and includes them in report"
    if not self._enabled: return

    # Saves the files
    gPad.SaveAs(self._path + '/' + self._figureFileName(name, thumb_fmt))
    gPad.SaveAs(self._path + '/' + self._figureFileName(name, vector_fmt))

    #logs the output in report
    self << "<A border=0 href=\"" + self._figureFileName(name, vector_fmt) + "\">" \
         << "<IMG src=\"" + self._figureFileName(name, thumb_fmt) + "\""+options\
         << "/></A>\n";

    self._figIndex += 1
  
  def close(self):
    if not self._enabled: return
    "Close the report output file"
    self._file.write("</BODY></HTML>")
    self._file.close()

  def printDict(self, inputDict, options = None):
    if not self._enabled: return
    if not isinstance(inputDict, dict):
      print ("HTML::Report::printDict was given not a dictionary")
      return

    if options == None: options = ""
    
    self << "<TABLE>{}\n".format(options)
    for entry in inputDict:
      self << "<TR><TD>" << str(entry) << "<TD>" << str(inputDict[entry])<<"\n"
    self << "</TABLE>\n\n"


  def enable(): 
    self._enabled = True
  def disable():
    self._enabled = False

  def flush(self):
    if not self._enabled: return
    self._file.flush()
    os.fsync(self._file.fileno())


  #internal variables
  _filename = None
  _path     = None
  _options  = None
  _file     = None
  _figIndex = None
  _myCanvas = None
  _enabled  = True


  br = "<BR/>\n"

