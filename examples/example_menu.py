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
from Tkinter import Toplevel

if __name__ == '__main__':
    gui = tkgen.gengui.Generator()
    root = gui.initialize('example_menu.json', title = 'Some test gui...')

    def hello():
        print 'Hello world'

    def open_popup():
        gui.toplevel('example_menu_dialog.json', title = 'A dialog')
        gui.button('cancel_dialog', close_popup)

    def close_popup():
        dialog = gui.find('dialog')
        dialog.master.destroy()

    def exit_app():
        root.destroy()

    # Traditional menu
    gui.create_menu({'Exit': exit_app}, name='File')
    some_menu = gui.create_menu({'Item': hello}, name='Menu')
    gui.create_menu({'Subitem': hello}, name='Submenu', parent=some_menu)
    gui.create_menu({'?': hello})

    # Popup menu
    popup_menu = gui.create_menu({'Foo':open_popup, 'Bar':open_popup}, popup=True)

    def popup(event):
        popup_menu.post(event.x_root, event.y_root)

    # attach popup to frame
    frame = gui.find('content')
    frame.bind("<Button-3>", popup)

    gui.button('cancel', exit_app)
    gui.button('ok', hello)

    root.mainloop()
