"""
Module with the basic class for the application window.
"""
import datetime
import itertools as it
# Use `TkAgg` backend to avoid conflicts between Matplotlib and Tkinter
import matplotlib
matplotlib.use("TkAgg")
import tkinter as tk
from ..core import database as db
from ..core import creditcards as cc
from ..core import utils as ut
from .custom_widgets import AutocompleteEntry

class Application(tk.Frame):
    """Define the basic window used to interface with the app."""

    def __init__(self, master=None):
        super().__init__(master, padx=50, pady=50)
        self.transactions = None
        self.categories = None
        self.suggestions = {}
        self.cursor = db.connect_to_database()
        self._load_data()
        self._gather_suggestions()
        self._create_widgets()

    def _load_data(self):
        """Connect to the database and get all the transaction info."""
        self.cursor.execute('SELECT * FROM transactions;')
        self.transactions = cc.load_credit_card_transactions(self.cursor)
        self.categories = self.transactions.columns

    def _gather_suggestions(self):
        """Automatically generate suggestions for existing categories."""
        for category in self.categories:
            # Don't give suggestions for dates or prices
            if 'date' in category or 'price' in category:
                continue
            self.suggestions[category] = set(self.transactions[category])

    def _create_widgets(self):
        """Add widgets and layout the app interface."""
        # Create an outer frame to hold the contents
        content = tk.Frame(self.master, padx=20, pady=20)
        content.pack()
        # Create the autcomplete entry boxes on top
        entry_frame = tk.Frame(content)
        entry_frame.pack()
        self.entries = {}
        row_counter = it.count(1)
        for category in self.categories:
            # Create an entry box for each category
            if category in self.suggestions:
                entry_sugg = self.suggestions[category]
                entry = AutocompleteEntry(entry_sugg, entry_frame)
            else:
                entry = tk.Entry(entry_frame)
            # Position the entry box and label
            row = next(row_counter)
            label_name = ut.format_category(category)
            tk.Label(entry_frame, text=label_name).grid(row=row, column=0,
                                                    sticky=tk.E)
            entry.grid(row=row, column=1)
            self.entries[category] = entry
        # Create a quit button at the bottom
        button_frame = tk.Frame(content)
        button_frame.pack(fill=tk.X, pady=(20,0))
        self.quit_button = tk.Button(button_frame, text='Exit',
                                     command=self.quit)
        self.quit_button.pack(side=tk.RIGHT)
        self.insert_button = tk.Button(button_frame, text='Insert',
                                       command=self._insert)
        self.insert_button.pack(side=tk.RIGHT)

    def _insert(self):
        """Insert the entered values into the database."""
        values = {}
        for category in self.categories:
            # Get the value for each entry category
            value = self.entries[category].get()
            if not value:
                # Don't allow empty inputs
                print(f'{ut.format_category(category)} must not be blank!')
                return
            if 'date' in category:
                value = ut.format_date(value)
            values[category] = value
        print(values)
