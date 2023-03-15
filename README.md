# Pyside Layout Tool

Pyside Layout Tool is a python application built to help Technical Artist and Tool Developers to make quick clean 
parameter layout to there supported application that has a python interpreter.

## Warning
  Tool is still under development and is going to go through consent updates.
   
  ### Metadata Functions
   
   - ```name()``` : return string name of the parameter.
   - ```label()``` : return string display name that is shown on layout.
   - ```callback()``` : return string of script or empty string.
   - ```type()``` : return namedtuple ```currentItem_name``` , ```currentItem_index```.
   - ```disable_when()``` : return string of expression or empty string.
   - ```hiden_when()``` : return string of expression or empty string.
   - ```invisible()``` : return bool.
   - ```eval()``` : return value of a parameter.
   - ```set_value(value)```: set value for parameter.
   
 ### Parameter Functions
  
   - ```bNeighbor()``` : return bool parameter as another parameter next to it.
   - ```default_value()``` : return string of default value of parameter.
  
  ### Folder Functions
  
   - ```tab_hide()```: return string of tab hide expression.
   - ```tab_disable()``` : return string of tab disable expression.

  ### Hide/Disable Expression
    For an expression to work for a parameter e.g :( { parameter_name == 5 } ).
    If you have experince with Houdini digital asset its the same format expression.
    
  ### Script Section
     
   - On Parameter/Folder Callback to work with script: ```ui.editor('Name of UI', 'Category Name').pyModule('Module Name').func()``` or
     ```self.pwd().pyModule('Module Name').func()```
   - Special arguments that can be passed to invoked callback function:
      - ```kwargs['parm']``` : return widget object the callback was invoked.
      - ```kwargs['layout']``` : return parent layout window object.
   - To get other parameter objects : ```ui.layout('Name of UI', 'Category Name').parm('parameter Name')```
   

 ### Extending PySide Layout Tool
   1. Make new Dictionary in Plugins
   2. Must have file *.uiplugin
      ```json
         "Categories":
         [
           {
             "Name": "Common",
             "Modules":
             [
                 "WidgetTestClass"
             ]
           }
         ]
      ```
   4. Add Plugin Folder name to UIEditorProject.uiproject
      ```json
         {
            "Name" : "TestingWidgetPlugin",
            "Enable" : true
         }
      ```
   - See Plugins/TestingWidgetPlugin for setup example.
  
   ```python
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
   ```
  ![Screenshot (434)](https://user-images.githubusercontent.com/19835724/166815862-54a6afee-ef4d-4fe3-8d63-4d20d2cd9d22.png)

# Known Issues 

  - importing modules from text editor will fail depending on scope.
    - text editor will be reworked completely with jedi or kite plugin. 
    
  ### Ramp
    - Not all interpolation are yet implemented.
    - Sometimes Ramp graph doesnt resize properly.
    - Callback not implemented.
    - Needs more testing.
