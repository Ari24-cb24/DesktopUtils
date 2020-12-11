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
    - ``dotenv``: Used for the .env file that saves the TOKENs for the APIs
    - ``pillow``: Used for the windows stray (OSX Support disabled)

- Used APIs
    - `Openweathermap <https://openweathermap.org>`_


#####################
Implemented functions
#####################

- Weather


#######################
Add your own extensions
#######################

#. Create a folder in the folder "plugins"
#. Create 3 files:
    - __init__.py
    - info.meda
    - YourWidgetName.py

#. Write the following in your files:
    - info.meda:
        - needs to contain the following layout!
        - ``NAME=Your plugin Name``
        - ``AUTHOR=Your nickname``
        - ``DESCRIPTION=A simple description about your widget``
        - ``VERSION=1.0``
        - ``MAIN=The filename for your Main file with a .py extension!``
        - ``CLASS=In your mainfile theres a class that DesktopUtils will access. Write that class name here!``
    - YourWidgetName.py
        - take a look at the example widget file
    - \_\_init\_\_.py:
        - in this file you need to import the main file and the package self like:
            - ``from plugins.packagename import myWidget``
            - and also
            - ``from plugins.packagename.myWidget import MyMainClass``

.. IMPORTANT:: If something isnt correct, your widget won't work!