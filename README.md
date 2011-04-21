
Create Tkinter GUIs from XML or JSON definition files
=====================================================

The idea behind this simple module is that you can define Tkinter GUIs in
either JSON or XML format. All value which can be configured for an widget can
be defined in those files. The module 'tkgen' has an Generator class which is
able to parse these files and return you a Tk root.

To use a JSON file as input:

    gui = tkgen.gengui.Generator()
    root = gui.initialize('ui.json', title = 'Some test gui...')
    root.mainloop()

Or XML:

    gui = tkgen.gengui.Generator()
    root = gui.initialize('ui.xml', type = 'xml', title = 'Some test gui...')
    root.mainloop()

Please see the examples in the 'examples/' directory for more details.

Feel free to play around with this - I do not guarantee that it is perfect nor
complete - Have Fun!

(c) 2011 tmetsch
