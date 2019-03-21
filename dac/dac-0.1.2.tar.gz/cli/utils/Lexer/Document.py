""" A Document is simply a collection of Blocks. """
# This is more for syntactical sugar purposes, but 
# in the future we may can add more advanced functionality
# at the document level.

class Document:
    def __init__(self):
        self.blocks = []

