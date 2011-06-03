
Create Tkinter GUIs from JSON definition files
==============================================

The idea behind this simple module is that you can define Tkinter GUIs in
a JSON file format. All value which can be configured for an widget can
be defined in those files. The module 'tkgen' has an Generator class which is
able to parse these files and return you a Tk root.

To use a JSON file as input:

    root = tkgen.gengui.TkJson('ui.json', title = 'Some test gui...')
    root.mainloop()

Please see the examples in the 'examples/' directory for more details on how to
use this package.

Module can be retrieved from [pypi](http://pypi.python.org/pypi/pytkgen/) as 
well:

    easy_install/pip install pytkgen

Some useful Tips
----------------

So since the GUI itself is defined in a JSON file you need to lookup the
widgets in your python code to do actual operations on them. The gengui module
offers some routines which will make your life easy:

  * get(name) - Returns the Tkinter widget object of the widget with the given
    name. Requires that a name was indeed defined in the definition file for
    this widget. Now that you have the object for an Tkinter widget you can do
    everything which is defined for this particular widget with it using known
    techniques.
    
  * button(name, cmd, [...]) - Associates a 'Button' widget with a command - For
    example: 'root.destroy'.
    
  * checkbox(name, [...]) - Returns an 'IntVar' for a 'Checkbox' so you can
    retrieve the value (0/1) to see if the User checked the box or not.
    
  * entry(name, [...]) - Returns a 'StringVar' for a Entry so you can retrieve
    and set the value of a Entry widget.
  
  * label(name) - Returns a 'StringVar' for a Label so you can retrieve and set
    the value of a Label widget.
  
  * create_from_file([...]) - Create a set of widgets from a file and add them
    to a given parent widget.
  
  * notebook([...]) - Adds a tab to a tkk Notebook widget which is itself
    defined by a JSON file.
  
  * treeview([...]) - Adds a item to a given treeview.
  
  * toplevel([...]) - Creates a toplevel dialog from a JSON definition file.

  * create_menu([...]) - Create new menus, popup menus or submenus on the fly.

  * xscroll and yscroll([...]) - Adds a Horinzontal/Vertical Scrollbar to a 
    widget.

Supported Attributes for Grid placement
---------------------------------------

On top of all attributes supported by a widget, the following attributes can be
used in the JSON files to refine the placement of widgets in the Grid Geometry
Manager:

  * row, column - Define the row and column in which the widget should appear 
    (default: 0).

  * rowspan, columnspan - Define if the widget should span across multiple rows
    or columns (default: 1).

  * rowweight, colweight, weight - Define the weight for a row or column or
    both (weight). If the weight is set the parent rows/columns are configured
    automatically to take care of the resizing. (default: 0).

  * padx, pady - X,Y padding for the widget (default: 2px).

  * sticky - Defines the sticky attribute as string (default: 'news').

Changelog
---------

1.4

  * Support for sticky attribute in the JSON file

1.3

  * Code optimizations
  * Support for setting the focus of a widget
  * More 'supporting routines'

1.2

  * Support for creation of menus
  * Support for multiple frames in JSON
  * Support for ttk widgets (Treeview, Notebook, Separator, Progressbar, ...)
  * Resizing capabilities added (Weights can now be defined in the JSON file; 1 
    means the widget resize in general, rowweight=1 means it resize horizontal, 
    colweight=1 means it resize vertical; Values > 1 mean that this widget will
    resize 'faster' (See Tk documentation for more information)).

1.1

  * Initial

Feel free to play around with this - I do not guarantee that it is perfect nor
complete - Have Fun!

(c) 2011 tmetsch
