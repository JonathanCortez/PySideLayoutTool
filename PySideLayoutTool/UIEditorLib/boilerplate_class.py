from PySideLayoutTool.UIEditorLib.UIEditorFactory import WidgetFactory
from PySideLayoutTool.UIEditorLib.UIEditorProperty import UIProperty
import PySideLayoutTool.UIEditorLib.TemplateBuildClass as TemplateBuildClass
import PySideLayoutTool.UIEditorLib.LayoutTemplate as LayoutTemplate

# Base widget class template
"""
LayoutTemplate.ParmSetup : is for most common parameters.
LayoutTemplate.FolderSetup : is good for folder type templates.

"""


class NAMEClass(LayoutTemplate.SETUPTYPE):

    def __init__(self, parent=None):
        super(NAMEClass, self).__init__(parent)
        self._widget = NAMELayout.NAMELayoutClass()  # NAMELayoutClass is the layout class for your widget.
        self._layout.addWidget(self._widget)  # Add your widget to the layout.

    """
        UIProperty decorator which will add a widget info filler
        for the widget description.

        Current Widget Properties supported:
        - CheckProperty
        - ClampProperty
        - ComboProperty
        - DictionaryProperty
        - LineEditProperty
        
        example:
        @UIProperty(metaWidget='CheckProperty',label='Check Demo', category='Solo')
        def demo_check(self):
            pass
        
        functions with UIProperty decorator will be added to the widget properties.
        Keep noted functions with UIProperty decorator must have a pass statement. (No code)
        
        Can also make your own Property Widget and register to the system.

    """
    def PostUpdate(self):
        super(NAMEClass, self).PostUpdate()
        # Add any post update code here.

    def PreUpdate(self):
        pass
        # Before widget is added to the layout and values are given to it.


# Class for properly building the widget with the application.
"""
TemplateBuildClass.ParameterBuild: for most common parameters.
TempalteBuildClass.FolderBuild: good for folder types, handling items within items

"""


class NAMEBuild(TemplateBuildClass.BUILDTYPE):

    def widgetClass(self):
        return NAMEClass


"""
register() and unregister() are required for the plugin widget to be loaded.
"""

"""
Register widget to be shown in supported templates.
"""


def register():
    WidgetFactory.register('WIDGET LABEL', NAMEBuild)


def unregister():
    WidgetFactory.unregister('WIDGET LABEL')


#------------------------------

import PySide2.QtWidgets as QtWidgets


# Class to layout your widgets
class NAMELayoutClass(QtWidgets.QWidget):

    def __init__(self):
        super(NAMELayoutClass, self).__init__()
        self._base_layout = QtWidgets.QVBoxLayout()
        self._base_layout.setSpacing(0)
        self._base_layout.setContentsMargins(0, 0, 0, 0)

        self._hbox_layout = QtWidgets.QHBoxLayout()
        self._hbox_layout.setSpacing(0)
        self._hbox_layout.setContentsMargins(0, 0, 0, 0)

        self._line_widget = QtWidgets.QLineEdit('Testing')
        self._button_widget = QtWidgets.QPushButton("Push")

        self._hbox_layout.addWidget(self._line_widget)
        self._hbox_layout.addWidget(self._button_widget)

        self._base_layout.addLayout(self._hbox_layout)
        self.setLayout(self._base_layout)


#------------------------------

from PySideLayoutTool.UIEditorLib.UIEditorProperty import UICProperty, PropertyFactory, IWidgetProperties

@PropertyFactory.register('NAMEProperty')
class NAMEProperty(IWidgetProperties):

    def __init__(self):
        super(NAMEProperty, self).__init__()
        self._widget = None  # Add custom Widget here, this is the widget that will be added to the layout.
        self._layout.addWidget(self._widget)

    def override_default(self, defaults: tuple):
        pass

    def setValue(self, value):
        pass

    def value(self):
        return None
    """
    Add @UICProperty decorator to any function that you want to be a property value
    that can be accessed by Widget setup.
    
    example:
        Base WidgetSetup class has a property called invisible.
        
        @UIProperty(metaWidget='CheckProperty', label='Invisible', category='Setting')
        def invisible(self):
            pass
        
        And in PostUpdate() function we call the invisible() function to get the value.
        
        def PostUpdate(self):
            super(ExampleClass, self).PostUpdate()
            self.invisible().mark
            
        This will return a bool value of the invisible property which mark has the decorator @UICProperty.
    
    @UICProperty
    def example(self):
        return self._state
    """