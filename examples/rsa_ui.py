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

from Tkconstants import END
import tkgen.gengui

def euclid(a, b):
    """
    Euclid
    """

    if b == 0:
        return a
    else:
        return euclid(b, a % b)

def extended_euclid(a, b):
    """
    Extended Euclid
    """
    if b == 0:
        return [a, 1, 0]
    else:
        previous_d, previous_x, previous_y = extended_euclid(b, a % b)
        d, x, y = (previous_d, previous_y, previous_x - a // b * previous_y)
        return [d, x, y]

def generate_keys(p, q):
    """
    Generation of public and private keys...
    """

    n = p * q
    m = (p - 1) * (q - 1)

    e = long(2)
    while e < m:
        if euclid(e, m) == 1:
            break
        else:
            e = e + 1

    dd, x, y = extended_euclid(m, e)
    if y > 0:
        d = y
    else:
        d = y % m

    return [(e, n), (d, n)]

if __name__ == '__main__':
    gui = tkgen.gengui.Generator()
    root = gui.initialize('rsa_ui.json', title = 'RSA example')

    p_entry = gui.find('pub')
    pr_entry = gui.find('priv')
    c_entry = gui.find('c_msg')
    d_entry = gui.find('d_msg')

    def ok(event=None):
        p = long(p_v.get())
        q = long(q_v.get())
        msg = long(m_v.get())

        pub_key, priv_key = generate_keys(p, q)

        e, n = pub_key
        d, n = priv_key
        crypted = (msg ** e) % n
        original = crypted ** d % n

        p_entry.config(state = 'normal')
        p_entry.delete(0, END)
        p_entry.insert(END, repr(e) + ', ' + repr(n))
        p_entry.config(state = 'disabled')

        pr_entry.config(state = 'normal')
        pr_entry.delete(0, END)
        pr_entry.insert(END, repr(d) + ', ' + repr(n))
        pr_entry.config(state = 'disabled')

        c_entry.config(state = 'normal')
        c_entry.delete(0, END)
        c_entry.insert(END, crypted)
        c_entry.config(state = 'disabled')

        d_entry.config(state = 'normal')
        d_entry.delete(0, END)
        d_entry.insert(END, original)
        d_entry.config(state = 'disabled')

    p_v = gui.entry('p', focus=True)
    q_v = gui.entry('q')
    m_v = gui.entry('msg', key='<Return>', cmd=ok)

    # add button behaviour
    gui.button('ok', ok)
    gui.button('exit', root.destroy)

    root.mainloop()
