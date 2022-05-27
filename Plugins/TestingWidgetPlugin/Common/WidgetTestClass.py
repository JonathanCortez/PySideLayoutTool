from PySideLayoutTool.UIEditorLib.UIEditorFactory import WidgetFactory
from PySideLayoutTool.UIEditorLib import LayoutTemplate, TemplateBuildClass
from PySideLayoutTool.UIEditorLib.UIEditorProperty import UIProperty
from PySide2 import QtWidgets

# Class to layout your widgets
class WidgetDemoLayout(QtWidgets.QWidget):

    def __init__(self):
        super(WidgetDemoLayout, self).__init__()
        self._base_layout = QtWidgets.QVBoxLayout()
        self._base_layout.setSpacing(0)
        self._base_layout.setContentsMargins(0,0,0,0)

        self._hbox_layout = QtWidgets.QHBoxLayout()
        self._hbox_layout.setSpacing(0)
        self._hbox_layout.setContentsMargins(0, 0, 0, 0)

        self._line_widget = QtWidgets.QLineEdit('Testing')
        self._button_widget = QtWidgets.QPushButton("Push")

        self._hbox_layout.addWidget(self._line_widget)
        self._hbox_layout.addWidget(self._button_widget)

        self._base_layout.addLayout(self._hbox_layout)
        self.setLayout(self._base_layout)



# Base widget class template
"""
LayoutTemplate.ParmSetup : is for most common parameters.
LayoutTemplate.FolderSetup : is good for folder type templates.

"""
class WidgetDemoClass(LayoutTemplate.ParmSetup):

    def __init__(self,parent=None):
        super(WidgetDemoClass, self).__init__(parent)
        self._widget = WidgetDemoLayout()
        self._layout.addWidget(self._widget)


    """
        UIProperty decorator which will add a widget info filler
        for the widget description.
        
        Current Widget Properties supported:
        - CheckProperty
        - ClampProperty
        - ComboProperty
        - DictionaryProperty
        - LineEditProperty
        
        Can also make your own Property Widget and register to the system.
        
    """

    @UIProperty(metaWidget='CheckProperty',label='Check Demo', category='Solo')
    def demo_check(self):
        pass




# Class for properly building the widget with the application.
"""
TemplateBuildClass.ParameterBuild: for most common parameters.
TempalteBuildClass.FolderBuild: good for folder types, handling items within items

"""
class WidgetDemoBuild(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return WidgetDemoClass


"""
Register widget to be shown in supported templates.
"""
def register():
    WidgetFactory.register('Demo Widget', WidgetDemoBuild)