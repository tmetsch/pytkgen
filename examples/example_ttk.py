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

    root = tkgen.gengui.TkJson('example_ttk.json', title='Some test gui...')

    # add tabs to the notebook
    notebook = root.get('notebook')
    root.notebook(notebook, 'example_ttk_notebook_tab_1.json', name='Tab 1')
    root.notebook(notebook, 'example_ttk_notebook_tab_2.json', name='Tab 2')

    # alter an entry in a notebook tab
    text = root.label('foo')
    text.set('The second Tab has a Treeview in it...')

    # progressbar
    progressbar = root.get('progressbar')
    progressbar.start()

    # treeview interaction
    treeview = root.get('treeview')
    treeview.heading('#0', text='1')
    treeview.heading('0', text='2')
    treeview.heading('1', text='3')

    item = root.treeview(treeview, 'item', ['foo', 'bar'])
    leaf = root.treeview(treeview, 'leafitem', ['foo', 'bar'], parent=item)
    root.treeview(treeview, 'first_item', ['foo', 'bar'], index=0)

    # menu
    root.create_menu({'Exit': exit_app}, name='File')

    root.mainloop()
