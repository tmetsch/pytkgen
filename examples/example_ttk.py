#!/usr/bin/python

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

import tkgen.gengui

if __name__ == '__main__':

    def exit_app():
        root.destroy()

    gui = tkgen.gengui.Generator()
    root = gui.initialize('example_ttk.json', title = 'Some test gui...')

    # add tabs to the notebook
    notebook = gui.find('notebook')
    gui.notebook(notebook, 'example_ttk_notebook_tab_1.json', name='Tab 1')
    gui.notebook(notebook, 'example_ttk_notebook_tab_2.json', name='Tab 2')

    # alter an entry in a notebook tab
    gui.find('foo').config(text="The second Tab has a Treeview in it...")

    # progressbar
    progressbar = gui.find('progressbar')
    progressbar.start()

    # treeview interaction
    treeview = gui.find('treeview')
    treeview.heading('#0', text='1')
    treeview.heading('0', text='2')
    treeview.heading('1', text='3')

    item = gui.treeview(treeview, 'item', ['foo', 'bar'])
    leaf = gui.treeview(treeview, 'leafitem', ['foo', 'bar'], parent=item)
    gui.treeview(treeview, 'first_item', ['foo', 'bar'], index=0)

    # menu
    gui.create_menu({'Exit': exit_app}, name='File')

    root.mainloop()
