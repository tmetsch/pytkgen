#
# Copyright (c) 2011. All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301  USA
#
"""
Module for easy creation of Tkinter GUIs.

Created on Apr 21, 2011

@author: tmetsch
"""

from Tkinter import Tk, IntVar, StringVar
import Tkinter
import ttk
import json,os


def _contains_dict(items):
    """
    Checks if a set of items contains a dictionary.

    items -- The set of items to test.
    """
    result = False
    for item in items.keys():
        if isinstance(items[item], dict):
            result = True
            break
    return result


def _contains_list(items):
    """
    Checks if a set of items contains a list.

    items -- The set of items to test.
    """
    result = False
    for item in items.keys():
        if isinstance(items[item], list) and item is not item.lower():
            # the .lower check ensures that I can have attribute lists
            result = True
            break
    return result


class TkJson(Tk):
    """
    Simple class which wraps Tk and uses some JSON to contruct a GUI.
    """

    menu = None
    widgets = {}

    def __init__(self, filename, title='Tk', preferTk=True):
        """
        Initialize a Tk root and created the UI from a JSON file.

        Returns the Tk root.
        """
        # Needs to be done this way - because base class do not derive from
        # object :-(
        Tk.__init__(self)
        self.preferTk=preferTk
        self.title(title)
        
        user_interface = json.load(open(filename)) if os.path.isfile(filename) else json.loads(filename)

        self.create_widgets(self, user_interface)

    def create_widgets(self, parent, items):
        """
        Creates a set of Tk widgets.
        """
        for name in items.keys():
            current = items[name]
            if isinstance(current,
                          dict) and not _contains_list(
                              current) and not _contains_dict(current):
                self._create_widget(name, parent, current)

            elif isinstance(current, dict) and _contains_list(current):
                widget = self._create_widget(name, parent, current)
                if not widget: break

                self.create_widgets(widget, current)
            elif isinstance(current, dict) and _contains_dict(current):
                widget = self._create_widget(name, parent, current)
                if not widget: break

                self.create_widgets(widget, current)
            elif isinstance(current, list):
                for item in current:
                    self.create_widgets(parent, {name: item})

    def _create_widget(self, name, parent, desc):
        """
        Tries to resolve the widget from Tk and create it.

        Returns the newly created widget.

        name -- Name of the widget.
        parent -- The parent widget.
        desc -- Dictionary containing the description for this widget.
        """
        position, weight, padding, opt = self._get_options(desc)

        try:
            widget_factory = getattr(Tkinter, name) if self.preferTk else getattr(ttk, name)
        except AttributeError:
            import traceback
            traceback.print_exc()
            try:
                widget_factory = getattr(ttk, name) if self.preferTk else getattr(Tkinter, name)
            except AttributeError as e:
                import traceback
                traceback.print_exc()
                raise AttributeError('Neither Tkinter nor ttk have a widget named: ', name)

        while True:
         try:
          widget = widget_factory(parent, **opt)
          break
         except Exception as e:
          print e
          if len(opt)==0: break
          del opt[str(e).split()[2][2:-1]]
          # widget = widget_factory(parent,**opt)

        widget.grid(row=position[0],
                    column=position[1],
                    columnspan=weight[0],
                    rowspan=weight[1],
                    sticky=padding[2],
                    padx=padding[0],
                    pady=padding[1])

        # propaget size settings when needed.
        if 'width' in opt or 'height' in opt:
            widget.grid_propagate(0)

        # set parent weight of the cells
        if weight[2] > 0:
            parent.rowconfigure(position[0], weight=weight[2])
        if weight[3] > 0:
            parent.columnconfigure(position[1], weight=weight[3])

        self.widgets[widget._name] = widget

        return widget

    def _get_options(self, dictionary):
        """
        Extracts the needed options from a dictionary.

        dictionary -- Dictionary with all the options in it.
        """
        options = {}

        row = 0
        column = 0

        colspan = 1
        rowspan = 1
        rowweight = 0
        colweight = 0

        padx = 2
        pady = 2

        sticky = 'news'

        if 'row' in dictionary:
            row = dictionary['row']
            dictionary.pop('row')
        if 'column' in dictionary:
            column = dictionary['column']
            dictionary.pop('column')

        if 'columnspan' in dictionary:
            colspan = dictionary['columnspan']
            dictionary.pop('columnspan')
        if 'rowspan' in dictionary:
            rowspan = dictionary['rowspan']
            dictionary.pop('rowspan')
        if 'rowweight' in dictionary:
            rowweight = dictionary['rowweight']
            dictionary.pop('rowweight')
        if 'colweight' in dictionary:
            colweight = dictionary['colweight']
            dictionary.pop('colweight')
        if 'weight' in dictionary:
            colweight = dictionary['weight']
            rowweight = dictionary['weight']
            dictionary.pop('weight')

        if 'padx' in dictionary:
            padx = dictionary['padx']
            dictionary.pop('padx')
        if 'pady' in dictionary:
            pady = dictionary['pady']
            dictionary.pop('pady')
        if 'sticky' in dictionary:
            sticky = dictionary['sticky']
            dictionary.pop('sticky')

        for key in dictionary.keys():
            if not isinstance(dictionary[key],
                              dict) and not isinstance(dictionary[key], list):
                options[str(key)] = str(dictionary[key])
            elif isinstance(dictionary[key], list) and key == key.lower():
                # so we have an attribute list...
                options[str(key)] = dictionary[key]

        return [row, column], [colspan, rowspan, rowweight, colweight], [padx, pady, sticky], options

    ##
    # Rest is public use :-)
    ##

    def button(self, name, cmd, focus=False):
        """
        Associate a Tk widget with a function.

        name -- Name of the widget.
        cmd -- The command to trigger.
        focus -- indicates wether this item has the focus.
        """
        item = self.get(name)
        item.config(command=cmd)

        if focus:
            item.focus_set()

    def checkbox(self, name, focus=False):
        """
        Associates a IntVar with a checkbox.

        name -- Name of the Checkbox.
        focus -- indicates wether this item has the focus.
        """
        var = IntVar()
        item = self.get(name)
        item.config(variable=var)

        if focus:
            item.focus_set()

        return var

    def entry(self, name, key=None, cmd=None, focus=False):

        """
        Returns the text of a TK widget.

        name -- Name of the Tk widget.
        key -- Needed if a key should be bound to this instance.
        cmd -- If key is defined cmd needs to be defined.
        focus -- Indicates wether this entry should take focus.
        """
        var = StringVar()

        item = self.get(name)
        item.config(textvariable=var)

        if focus:
            item.focus_set()

        if key is not None and cmd is not None:
            item.bind(key, cmd)

        return var

    def label(self, name):
        """
        Associate a StringVar with a label.

        name -- Name of the Label.
        """
        var = StringVar()
        item = self.get(name)
        item.config(textvariable=var)
        return var

    def get(self, name):
        """
        Find a Tk widget by name and return it.
        """
        if name in self.widgets.keys():
            return self.widgets[name]
        else:
            raise KeyError('Widget with the name ` ' + name + ' ` not found.')

    def xscroll(self, widget_name, scrollbar_name):
        """
        Add a horizontal scrollbar to a widget.

        widget_name -- name of the widget.
        scollbar_name -- name of the scrollbar.
        """
        widget = self.get(widget_name)
        scrollbar = self.get(scrollbar_name)

        widget.config(xscrollcommand=scrollbar.set)
        scrollbar.config(command=widget.xview)

    def yscroll(self, widget_name, scrollbar_name):
        """
        Add a vertical scrollbar to a widget.

        widget_name -- name of the widget.
        scollbar_name -- name of the scrollbar.
        """
        widget = self.get(widget_name)
        scrollbar = self.get(scrollbar_name)

        widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=widget.yview)

    def create_menu(self, commands, name=None, parent=None, popup=False):
        """
        Creates a menu(entry) if non is available. Returns the created menu so
        you can define submenus.

        commands -- dict with 'label':'command' structure.
        name -- Needs to be provided if it is a dropdown or submenu.
        parent -- Needs to be provided if it is a submenu.
        popup -- indicates if it is an popup menu or not (Default: False)
        """
        if self.menu is None and popup is False:
            # If no menu exists create one and add it to the Tk root.
            self.menu = Tkinter.Menu(self, tearoff=0)
            self.config(menu=self.menu)

        if name is None and parent is None and popup is False and len(commands.keys()) > 0:
            # Just create a Menu entry.
            for key in commands:
                self.menu.add_command(label=key, command=commands[key])
            return self.menu
        elif name is not None and popup is False and len(commands.keys()) > 0:
            if parent is None:
                # Create a top-level drop down menu.
                tmp_menu = Tkinter.Menu(self.menu, tearoff=0)
                self.menu.add_cascade(label=name, menu=tmp_menu)
            else:
                # Create a submenu.
                tmp_menu = Tkinter.Menu(parent, tearoff=0)
                parent.add_cascade(label=name, menu=tmp_menu)

            for key in commands:
                tmp_menu.add_command(label=key, command=commands[key])

            return tmp_menu
        elif popup is True and len(commands.keys()) > 0:
            tmp_menu = Tkinter.Menu(self, tearoff=0)
            for key in commands:
                tmp_menu.add_command(label=key, command=commands[key])

            return tmp_menu
        else:
            raise AttributeError('Invalid parameters provided')

    # Move?

    def create_from_file(self, parent, filename):
        """
        Create a set of widgets and add them to the given parent.

        parent -- The parent of the to be created widgets.
        filename -- The JSON definition file.
        """
        ui_file = open(filename)
        definition = json.load(ui_file)
        self.create_widgets(parent, definition)

    def notebook(self, parent, filename, name='Tab'):
        """
        Add a tab to a tkk notebook widget.

        parent -- The parent notebook widget instance.
        filename -- The file which describes the content of the tab.
        name -- The name of the tab.
        """
        frame = Tkinter.Frame()
        self.create_from_file(frame, filename)
        parent.add(frame, text=name)

    def toplevel(self, filename, title='Dialog'):
        """
        Open a Toplevel widget.

        parent -- The parent notebook widget instance.
        title -- The title for the dialog.
        """
        dialog = Tkinter.Toplevel()
        dialog.title(title)
        self.create_from_file(dialog, filename)
        dialog.grid()
        return dialog

    def treeview(self, treeview, name, values, parent='', index=0):
        """
        Adds an item to a treeview.

        treeview -- The treeview to add the items to.
        name -- The name of the value.
        values -- The values itself.
        parent -- Default will create root items, if specified create a leaf.
        index -- If index < current # of items - insert at the top.
        """
        return treeview.insert(parent, index, text=name, values=values)
