"""Modules for creating a widget-based user interface. See the examples folder 
for sample scripts that use this module."""

# The basestring class was removed in Python 3, but we want to keep it to maintain
# compatibility with previous versions of python.
try:
    __builtins__["basestring"]
except KeyError:
    __builtins__["basestring"] = str

from .app import App, Desktop
# html
from .area import SlideBox, ScrollArea, List
from .basic import Spacer, Color, Label, Image, parse_color
from .button import Icon, Button, Switch, Checkbox, Radio, Tool, Link
from .const import *
from .container import Container
from .deprecated import Toolbox, action_open, action_setvalue, action_quit, action_exec
from .dialog import Dialog, FileDialog
from .document import Document
from .errors import *
from .form import Form
from .group import Group
from .input import Input, Password
from .keysym import Keysym
from .menus import Menus
from .misc import ProgressBar
from .select import Select
from .slider import VSlider, HSlider, VScrollBar, HScrollBar
from .style import Style
from .surface import subsurface, ProxySurface
from .table import Table
from .textarea import TextArea
from .theme import Theme
from .widget import Widget

