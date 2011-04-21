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

from Tkconstants import W, E, N, S
from Tkinter import Tk, IntVar
import Tkinter
import json
import xml.etree.ElementTree as etree


'''
Simple class which wraps Tk and uses some XML/JSON to contruct a GUI...

Created on Apr 21, 2011

@author: tmetsch
'''
class Generator(object):

    def initialize(self, filename, type = 'json', title = 'Tk'):
        """
        Initialize a Tk root and created the UI from a XML/JSON file.

        Returns the Tk root.
        """
        root = Tk()
        root.title(title)

        if type is 'xml':
            ui = etree.parse(filename).getroot()

            self.create_frame_xml(root, ui)
        elif type is 'json':
            ui_file = open(filename)
            ui = json.load(ui_file)

            self.create_frame_json(root, ui)
        else:
            raise AttributeError('Type ' + type + ' not supported...')

        self.frame.grid()
        return root

    def create_frame_json(self, master, element):
        """
        Optimized method to create a Tk frame from a JSON tree :-)
        """

        for item in element.keys():
            if item == 'Frame':
                self.frame = Tkinter.Frame(master)
                widget = self.frame
            else:
                options = {}
                row = 0
                column = 0
                columnspan = 1
                for child in element[item]:
                    if not isinstance(element[item][child], dict) and not isinstance(element[item][child], list):
                        if str(child) == 'row':
                            row = int(element[item][child])
                        elif str(child) == 'column':
                            column = int(element[item][child])
                        elif str(child) == 'columnspan':
                            columnspan = int(element[item][child])
                        else:
                            options[str(child)] = str(element[item][child])

                widget_factory = getattr(Tkinter, item)
                widget = widget_factory(master, **options)
                widget.grid(row = row, column = column, columnspan = columnspan,
                            sticky = W + E + N + S,
                            padx = 2,
                            pady = 2)

            for child in element[item]:
                if isinstance(element[item][child], list):
                    for sub_item in element[item][child]:
                        sub_element = {child: sub_item}
                        self.create_frame_json(widget, sub_element)
                elif isinstance(element[item][child], dict):
                    sub_element = {child: element[item][child]}
                    self.create_frame_json(widget, sub_element)

    def create_frame_xml(self, master, element):
        """
        Optimized method to create a Tk frame from a XML tree :-)

        Original Idea: (c) 2003 Fredrik Lundh
        Original source: http://effbot.org/zone/element-tkinter.htm
        """

        if element.tag == 'Frame':
            self.frame = Tkinter.Frame(master, **element.attrib)
            for subelement in element:
                widget, grid_info = self.create_frame_xml(self.frame, subelement)
                widget.grid(column = grid_info[0],
                            row = grid_info[1],
                            columnspan = grid_info[2],
                            sticky = W + E + N + S,
                            padx = 2,
                            pady = 2)

        else:
            options = element.attrib
            if 'column' in options.keys():
                col = options['column']
                options.pop('column')
            if 'row' in options.keys():
                row = options['row']
                options.pop('row')
            if 'columnspan' in options.keys():
                colspan = options['columnspan']
                options.pop('columnspan')
            else:
                colspan = 1

            widget_factory = getattr(Tkinter, element.tag)
            widget = widget_factory(master, **options)

            for subelement in element:
                subwidget, grid_info = self.create_frame_xml(widget, subelement)
                subwidget.grid(column = grid_info[0],
                               row = grid_info[1],
                               columnspan = grid_info[2],
                               sticky = W + E + N + S,
                               padx = 2,
                               pady = 2)

            return widget, [col, row, colspan]

    def button(self, name, cmd):
        """
        Associate a Tk widget with a function.
        """
        item = self._find_by_name(self.frame, name)
        item.config(command = cmd)

    def checkbox(self, name):
        """
        Associates a IntVar with a checkbox.

        name -- Name of the Checkbox
        """
        c = IntVar()
        item = self._find_by_name(self.frame, name)
        item.config(variable = c)
        return c

    def entry(self, name):
        """
        Returns the text of a TK widget.

        name -- Name of the Tk widget.
        """
        item = self._find_by_name(self.frame, name)
        return item.get()

    def find(self, name):
        """
        Find a Tk widget by name and return it.
        """
        result = self._find_by_name(self.frame, name)
        if result is None:
            raise KeyError('Tkinter widget with name "' + name + '" not found.')
        return result

    def _find_by_name(self, parent, name):
        """
        Recursively find a item by name.

        Needs to be recursive because of frames in frames in frames in ... :-)
        """
        items = parent.children
        result = None
        if name in items.keys():
            return items[name]
        else:
            for key in items.keys():
                if hasattr(items[key],
                           'children') and len(items[key].children) > 0:
                    result = self._find_by_name(items[key], name)
                    if result is not None:
                        break

        return result
