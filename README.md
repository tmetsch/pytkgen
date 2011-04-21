
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

Please see the examples in the 'examples/' directory for more details on how to
use this package.

Module can be retrieved from [pypi](http://pypi.python.org/pypi/pytkgen/) as 
well:

    easy_install/pip install pytkgen

Some useful Tips
----------------

So since the GUI itself is defined in a XML or JSON file you need to lookup the
widgets in your python code to do actual operations on them. The gengui module
offers some routines which will make your life easy:

  * find(name) - Returns the Tkinter widget object of the widget with the given
    name. Requires that a name was indeed defined in the definition file for
    this widget. Now that you have the object for an Tkinter widget you can do
    everything which is defined for this particular widget with it using known
    techniques.
    
  * button(name, cmd) - Associates a 'Button' widget with an command - For
    example: 'root.destroy'.
    
  * checkbox(name) - Returns an 'IntVar' for a 'Checkbox' so you can retrieve
    the value (0/1) to see if the User checked the box or not.
    
  * entry(name) - Returns the text of an 'Entry' widget.

Feel free to play around with this - I do not guarantee that it is perfect nor
complete - Have Fun!

(c) 2011 tmetsch
