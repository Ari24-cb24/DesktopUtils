.. |br| raw:: html

    <br/>

************
DesktopUtils
************

###################
General Information
###################

- Author: Ari24
- License: MIT
- Language: Python 3.7
- Required python packages:  
    - ``dotenv``: Used for the .env file that saves the TOKENs for the APIs or other config stuff (we'll use yaml in the future)
    - ``pillow``: Used for the windows stray (OSX Support disabled)

- Used APIs
    - `Openweathermap <https://openweathermap.org>`_


#####################
Implemented plugins
#####################

- Weather


#######################
Add your own Widgets!
#######################

**Create a folder in the folder "plugins" named like your plugin**


Create 3 files in it:

- __init__.py
- info.meda
- <YourWidgetName>.py

|br|
**info.meda** (an information file for the pluginmanager):

.. code-block::

    NAME=Your plugin Name
    AUTHOR=Your nickname
    DESCRIPTION=A simple description about your Widget
    VERSION=1.0
    MAIN=The filename for your Main file with a .py extension!
    CLASS=In your mainfile theres a class that DesktopUtils will access. Write that class name here!

|br|
**<YourWidgetName>.py** (Main file for your Widget):
This one is your main file. You need to import the following packages:

- ``from Widget import Widget``
- ``import tkinter``

.. important::

    Your main class must inherit from the Widget class!

Ill show you an example of a Widget class and then explain all the things.

.. code-block:: python

    import tkinter as tk
    from Widget import Widget

    class ExampleWidget(Widget):
        # These are only default parameters. You don't need to set them every time!
        REFRESH = True
        RESIZE = [False, False]
        START_POS = [0, 0]
        SIZE = [200, 200]
        BAR_COLOR = "black"

        def __init__(self, root):
            super().__init__(root)

            self.frame = tk.Frame(root, width=200, height=200)
            self.dummy_button = tk.Button(self.frame, text="Hallo Welt!")

        def run(self):
            self.dummy_button.pack()

            self.frame.pack()
            self.root.mainloop()

        def refresh(self):
            self.dummy_button.configure(text="Foo Bar!")


^^^^^^^^^^^
Explanation
^^^^^^^^^^^

.. code-block:: python

    import tkinter as tk
    from Widget import Widget

So I don't think I need to explain these import statements. DesktopUtils works with tkinter.

|br|

.. code-block:: python

    class ExampleWidget(Widget):
        # These are only default parameters. You don't need to set them every time!
        REFRESH = True
        RESIZE = [False, False]
        START_POS = [0, 0]
        SIZE = [200, 200]
        BAR_COLOR = "black"

So if you define your Widget, the class must inherit from the Widget class.
You can also set some PRE_START Parameters as seen above:

- ``REFRESH`` Default: True, Type: Boolean, If the Widget should be refreshed.
- ``RESIZE`` Default: [False, False], Type: List[Boolean], If the Widget is resizeable. First argument defines width axis and second argument defines height axis.
- ``START_POS`` Default: [0, 0], Type: List[Integer], The start position of the Widget. Default is in the left upper corner of the screen.
- ``SIZE`` Default: [200, 200], Type: List[Integer], The start size of your Widget.
- ``BAR_COLOR`` Default: "black", Type: String, The color of the bar of your Widget. Needs to be a tkinter color!

|br|

.. code-block:: python

    def __init__(self, root):
        super().__init__(root)

        self.frame = tk.Frame(root, width=200, height=200)
        self.dummy_button = tk.Button(self.frame, text="Hallo Welt!")

So the class is initialized here. You need to add the parameter root because the pluginmanager is going to deliver you that parameter.

.. important::

    PLEASE, DO NOT USE THE ROOT AS YOUR SURFACE. CREATE A FRAME, LET THE SURFACE BE THE ROOT AND USE THE FRAME AS THE ROOT!


After that you need to call the ``super()`` method because you inherited from the Widget class. Add the root as an argument to the ``super().__init__`` function!

And the rest... Is just normal variable initialization.

|br|

.. code-block:: python

    def run(self):
        self.dummy_button.pack()

        self.frame.pack()
        self.root.mainloop()

This is the run function. It's the first function of your Widget that is called when the Widget is started.


.. important::

    You need to call the mainloop on the root to let your window appear.

|br|

.. code-block:: python

    def refresh(self):
        self.dummy_button.configure(text="Foo Bar!")

You only need this function if you set the PRE_START Parameter ``REFRESH`` to True.
This function is called every x seconds. You can use it to refresh your Widget.

The number of seconds is defined in the .env file (the current config file).
You can change it anytime!

|br|

**\_\_init\_\_.py** (Important for the pluginmanager to load all your classes):

In this file you need to import your

- Main file
- All other files
- All defined classes in your files

Here's an example/preset:

.. code-block:: python

    from plugins.<packagename> import <MyWidgetName>  # importing the main file. It's important to name your main File like the plugin!
    from plugins.<packagename>.myMainFile import MyMainClass  # importing the main class
    from plugins.<packagename>.myWidget import MySecondClass  # importing some other classes defined in the main file
    from plugins.<packagename>.myWidget import MyThirdClass   # importing some other classes defined in the main file

    from plugins.<packagename> import mySecondFile  # importing some other files used from your plugin
    from plugins.<packagename>.mySecondFile import MyClassOne  # importing all of the classes in mySecondFile
    from plugins.<packagename>.mySecondFile import MyClassTwo  # importing all of the classes in mySecondFile
    from plugins.<packagename>.mySecondFile import MyClassThree  # importing all of the classes in mySecondFile

    """
    And so on...
    you get it
    """

.. IMPORTANT:: If something isn't correct, your Widget won't work!