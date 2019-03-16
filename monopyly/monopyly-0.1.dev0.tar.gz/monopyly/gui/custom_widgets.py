"""
A module containing custom Tkinter widgets.

This module contains custom Tkinter widgets to be used with the monopyly
interface. Currently, this is only an Autocomplete Entry widget that subclasses
the Tkinter Entry widget. It provides a dropdown menu of suggestions. The code
is adapted from an ActiveState recipe, found at:

http://code.activestate.com/recipes/578253-an-entry-with-autocompletion-for-the-tkinter-gui/

"""
import tkinter as tk
import re

suggestions = ['a', 'actions', 'additional', 'also', 'an', 'and', 'angle',
               'are', 'as', 'be', 'bind', 'bracket', 'brackets', 'button',
               'can', 'cases', 'configure', 'course', 'detail', 'enter',
               'event', 'events', 'example', 'field', 'fields', 'for', 'give',
               'important', 'in', 'information', 'is', 'it', 'just', 'key',
               'keyboard', 'kind', 'leave', 'left', 'like', 'manager', 'many',
               'match', 'modifier', 'most', 'of', 'or', 'others', 'out', 'part',
               'simplify', 'space', 'specifier', 'specifies', 'string;', 'that',
               'the', 'there', 'to', 'type', 'unless', 'use', 'used', 'user',
               'various', 'ways', 'we', 'window', 'wish', 'you']

class AutocompleteEntry(tk.Entry):
    """
    Create an entry box with a dropdown menu of autocomplete options.

    Provides the capability to have an entry box that provides autocomplete
    suggestions based on the current input. Values can be selected from the
    dropdown menu using the arrow keys.

    Parameters
    ––––––––––
    suggestions : list
        A list of all suggestions that could possibly be provided to the user.
    """

    def __init__(self, suggestions, *args, **kwargs):
        # Subclasses the tkinter Entry widget
        super().__init__(*args, **kwargs)
        # Set the list of possible suggestions to be searched
        self.suggestions = suggestions
        # Sets the value of the entry box to a StringVar for easy updating
        var = tk.StringVar()
        var.set(self['textvariable'])
        self.var = self['textvariable'] = var
        # Change the variable state each time the entry box value is modified
        self.var.trace('w', self._change_state)
        # Right arrow key, tab, and enter make selection
        self.bind("<Right>", self._make_selection)
        self.bind("<Return>", self._make_selection)
        self.bind("<Tab>", self._make_selection)
        # Up/down arrow keys move highlight
        self.bind("<Up>", self._up)
        self.bind("<Down>", self._down)
        # Create a flag to indicate whether the suggestions listbox is showing
        self.showing_lb = False

    def _change_state(self, name, index, mode):
        """Update the state of the entry (and provide new suggestions)."""
        if self.var.get() == '':
            # The entry box became empty, so remove the listbox of suggestions
            try:
                self.lb.destroy()
            except AttributeError:
                # A listbox object didn't exist, so we can't destroy it
                pass
            self.showing_lb = False
        else:
            # Check if any words match the current pattern
            words = self._comparison()
            if words:
                if not self.showing_lb:
                    # Create a new list box of suggestions below the entry box
                    self.lb = tk.Listbox(self.master)
                    entry_box_left_x = self.winfo_x()
                    entry_box_top_y = self.winfo_y()
                    entry_box_height = self.winfo_height()
                    entry_box_bottom_y = entry_box_top_y + entry_box_height
                    self.lb.place(x=entry_box_left_x, y=entry_box_bottom_y)
                    # Right arrow key, enter, and double-click make selection
                    self.lb.bind("<Double-Button-1>", self._make_selection)
                    self.lb.bind("<Right>", self._make_selection)
                    self.lb.bind("<Return>", self._make_selection)
                    self.lb.bind("<Tab>", self._make_selection)
                    # Indicate that the listbox is now showing
                    self.showing_lb = True
                # Clear the listbox of all current entries
                self.lb.delete(0, tk.END)
                # Update the listbox with each word that matches
                for w in words:
                    self.lb.insert(tk.END, w)
                # Make the listbox height as long as matching words
                self.lb['height'] = len(words)
            else:
                # No matching words were found, remove the suggestion listbox
                if self.showing_lb:
                    self.lb.destroy()
                    self.showing_lb = False

    def _make_selection(self, event):
        """Make the selection from the listbox, and close the box."""
        if self.showing_lb:
            # Select the active element
            self.var.set(self.lb.get(tk.ACTIVE))
            # Close the listbox
            self.lb.destroy()
            self.showing_lb = False
            # Move the cursor to the end of the chosen word in the entry box
            self.icursor(tk.END)

    def _up(self, event):
        """Move the selector up."""
        if self.showing_lb:
            # Get the currently highlighted entries of the listbox
            cursor_locations = self.lb.curselection()
            if cursor_locations:
                index = cursor_locations[0]
            else:
                # Above the highest element; cursor is in the entry box
                index = -1
            if index != -1:
                # Only allow one element to be selected
                self.lb.selection_clear(index)
                # Move the index up one (one less than the current index)
                index -= 1
                self.lb.selection_set(index)
                self.lb.activate(index)

    def _down(self, event):
        """Move the selector up."""
        if self.showing_lb:
            # Get the currently highlighted entries of the listbox
            cursor_locations = self.lb.curselection()
            if cursor_locations:
                index = cursor_locations[0]
            else:
                # Above the highest element; cursor is in the entry box
                index = -1
            if str(index) != tk.END:
                # Only allow one element to be selected
                self.lb.selection_clear(index)
                # Move the index down one (one more than the current index)
                index += 1
                self.lb.selection_set(index)
                self.lb.activate(index)

    def _comparison(self):
        """Check the string pattern against the potential suggestions."""
        textvar = self.var.get().replace('(','\(').replace(')','\)')
        pattern = re.compile('.*' + textvar + '.*', re.IGNORECASE)
        return [_ for _ in self.suggestions if re.match(pattern, str(_))]

if __name__ == '__main__':
    # DEMO IF MODULE IS RUN DIRECTLY
    root = tk.Tk()
    # Create the autcomplete entry box
    entry = AutocompleteEntry(suggestions, root)
    # Position the box and surrounding elements
    entry.grid(row=0, column=0)
    tk.Label().grid(column=0)
    tk.Label().grid(column=0)
    tk.Label().grid(column=0)
    tk.Label().grid(column=0)
    tk.Button(text='Exit', command=root.quit).grid(column=0, rowspan=2)
    root.mainloop()
