# PySide Layout Tool

PySide Layout Tool is an open-source graphical user interface (GUI) tool developed using Python and the PySide2 library for creating and editing layouts in PySide-based applications. The tool provides a simple and intuitive interface for designing and manipulating widgets and layouts, which are the building blocks of PySide applications.



The PySide Layout Tool allows users to create, edit, and save layouts in various file formats, including JSON and XML. It also provides a preview mode that allows users to see how the layout will look. The tool provides a wide range of layout options, including grid layout, horizontal layout, vertical layout, and stacked layout.



The tool is designed to simplify the layout creation process and make it more efficient. Users can drag and drop widgets onto the canvas and adjust their position and size using the mouse. The tool also provides alignment and spacing options to help users create a neat and organized layout.



# Warning
  Tool is still under development and is going to go through consent updates.
  
# Unreal Engine Plugin
  Link : [UE PySide Layout Tool](https://www.unrealengine.com/marketplace/en-US/product/pyside-layout-tool)

  ## Road Map
   https://trello.com/b/5SFDvILa/pyside-layout-tool-development

## Parameter Types

  ### Button
    A clickable button. You can enter a script to run when the user clicks the button.

  ### Button Strip
    A horizontal strip of labeled options. The buttons can be mutually exclusive or individually set. See Make a button strip.

  ### Color
    A 3 float vector parameter with a UI for editing the value as a color. Channels use the suffixes rgb instead of 123.

  ### Color and Alpha
    A 4 float vector parameter with a UI for editing the value as a color with alpha channel. Channels use the suffixes rgba instead of 1234.
    
  ### File
    A string representing a file path, with a UI for choosing a file from disk.

  ### Float
    A single floating point value.

  ### Float Vector 2
    Two floating point values.

  ### Float Vector 3
    Three floating point values, for example a 3D position.

  ### Float Vector 4
    Four floating point values, 

  ### Folder
    A container for other parameters. Folders let you organize the node’s parameters. You can choose to present the folder in different ways, such as a tab, group box, or collapsible section. Adjacent tabs join together automatically.

  ### Integer
    A single integer value.

  ### Integer Vector 2
    Two integer values.

  ### Integer Vector 3
    Three integer values.

  ### Integer Vector 4
    Four integer values.

  ### Key-Value Dictionary
    Stores a table of string → string associations.

  ### Label
    A read-only line of text.

  ### Min/max Float
    Two floats representing a low and high. Channels use the suffixes min and max instead of 1 and 2. 

  ### Min/max Integer
    Two integers representing a low and high. Channels use the suffixes min and max instead of 1 and 2.

  ### RGBA Mask
    An integer bitmask created from a UI allowing the user to turn each of a red, green, blue, and alpha button on or off individually.

  ### Ramp (Color)
    A three float vector with a color ramp UI.

  ### Ramp (Float)
    A single float with a curve ramp UI.

  ### Separator
    Inserts a separator line into the UI to organize the parameters.

  ### String
    A text box for editing a string value.

  ### Toggle
    A checkbox for editing a boolean value.

## Parameter Description
- **Default** :
    - **Name** : Unique name that cannot be similar to other parameters. This is how a parameter can be found in the system/script. Name can not have spacing or special characters only ‘_’. 

    - **Label** : This is the display name for the parameter.

    - **Callback Script** : Runs this script when the value of this parameter changes. If the value in the field is one line, it is treated as a Python expression and evaluated. See Scripts tab

    - **Type** : The . This affects how the value is stored and how the parameter is presented to the user in the parameter editor interface.

    - **Help** : This is displayed as a tooltip when the user hovers over the parameter.


- **Expressions** :
    - **Disable When** : A rule for when this parameter should appear disabled/non-editable. This lets you set up parameters to dynamically disable based on the value of other parameters. See Disable when/Hide when syntax

    - **Hidden When** : A rule for when this parameter should not appear. This lets you set up parameters to dynamically hide themselves based on the value of other parameters. See Disable when/Hide when syntax.

    - **Tab Folder**
        - **Tab Hidden When** : A rule for when this parameter should not appear. This lets you set up parameters to dynamically hide themselves based on the value of other parameters. See Disable when/Hide when syntax.

        - **Tab Disable When** : A rule for when this parameter should appear disabled/non-editable. This lets you set up parameters to dynamically disable based on the value of other parameters. See Disable when/Hide when syntax.


- **Setting** :
    - **Invisible** : When this is on, the parameter is not shown in the Layout Display Window, but you can still read and write its value using expressions and scripts.

    - **Default** : Value that will be set on fresh layout or reset values.

    - **Horizontal Join** : Put this parameter and the next parameter in the same row in the Layout Display Window. Note that you can turn this on for more than one parameter in a row to layout three or more parameters horizontally. If all the “joined” parameters can’t fit in a line, they will wrap to the next line.

    - **Range** : The range for the slider in the interface. If you click the lock icon next to low and/or high value, the interface prevents the user from manually entering values lower and/or higher than this range.

    - **Tab Placements** : Changes where the tabs will be displayed.
        - Top : (Default) tabs are added and displayed on top of the border.
        - Left : Displays to the left side of the border.
        - Right : Displays to the right side of the border.

    - **Open On Start** : Collapsible Folder will alway be open when the Layout Display Window is open.


- **String Setting** : 
    - **Multi-line string** : Display this field as a multi-line editor instead of a single line text field. Note that all string parameters can hold multi-line text.


- **Combo/Menu Items** :
    - **Button Type** : 
        - Normal (Menu Only, Single Selection) : Display the parameter as a pop-up menu.
        - Normal Mini (Mini Menu Only, Single Selection) : Display the parameter as a “mini” pop-up menu. This style only shows a small button to open the menu, instead of showing the current value.
        - Toggle (Field + Multiple Selection Menu) : This setting is only useful for String parameters. If you choose it for an Integer parameter you will get the same UI as Replace (above). This treats the parameter value as a space-separated list of keywords. It shows a regular text field the user can manually edit, with a mini pop-up menu at the end from which they can choose items. Choosing an item adds its token to the list (or removes it if it is already there).
    - **Items** : 
        - Key label :  The text to display at the top of the left (key) column in the parameter UI. If you leave this blank, it uses “Key”.
        - Value label : The text to display at the top of the right (value) column in the parameter UI. If you leave this blank, it uses “Value”.

## Disable when/Hide when syntax
Often you want to dynamically show or enable parameters based on the values of other parameters. For example, you might have a checkbox that enables some feature, and only want to enable editing parameters related to that feature when the checkbox is on.
The Disable when and Hide when settings of a parameter let you set up when the parameter should be disabled or hidden. The value is a code using the syntax shown below to calculate whether to disable/hide based on other parameter values.

The general syntax is:</p>
``{ parm_name [operator] value ...} ...``</p>
    - One or more comparisons inside curly braces.</p>
    - Inside the curly braces are one or more comparisons with a parameter name, a comparison operator, and a value.</p>
    - The following comparison operators are available: ==, !=, <, >, >=, <=, =~ (matches pattern), !~ (doesn’t match pattern).</p>
        ```{ type == 1 count > 10 } { tolerance < 0.1 }```</p>
        You must put spaces around the comparison operator, otherwise it will not accept the rule. </p>
    - If there are multiple conditions (sets of curly braces), any of the conditions may be true to activate disabling/hiding.</p>
    For example, with the condition below, if the enablefeature checkbox parameter is on or the count parameter is more than 10, this parameter would be disabled/hidden:</p>
    ```{ type == 1 } { count > 10 }```</p>
    If there are multiple comparisons inside a set of curly braces, all the comparisons must be true for that condition to be true.</p>
    For example, with the condition below, if the enablefeature checkbox parameter is on and the count parameter is more than 10, this parameter would be disabled/hidden:</p>
    ```{ enablefeature == 1 count > 10 }```

## Make a button strip 
1. Go to Combo/Menu Items in parameter description.

2. Fill Items with Keys and Values.

3. Choose a Button Type.
    - For “Normal” strips, it returns the index of the selected item (starting from 0).
    - For “Toggle” (multiple selection) strips, it returns a bit field.

## Scripts Section
This tab lets you store scripts that are triggered by asset events.

On Parameter/Folder Callback to work with script : </p>
```ui.editor('Name of UI', 'Category Name').pyModule('Module Name').func()```</p>
```self.pwd().pyModule('Module Name').func()```

Special arguments that can be passed to invoked callback function: </p>
      ```kwargs['parm'] : return widget object whose callback script was invoked.```</p>
      ```kwargs['layout'] : return parent layout window object.```

To get other parameter objects : </p>
 ```ui.layout('Name of UI', 'Category Name').parm('parameter Name')```

![Screenshot 2023-03-20 012638](https://user-images.githubusercontent.com/19835724/230806623-d0f4a247-b003-404b-9ea3-450c9522f6ea.png)


## Extending PySide Layout Tool
 ### Settings
   1. Go to Setting in `Create Layout` window.
      - Go to Plugins section.
![Screenshot 2023-04-09 185330](https://user-images.githubusercontent.com/19835724/230806563-ae0c4993-e0ea-40e5-b762-b9b17b388ec1.png)
   2. In Plugins display section, click `New Plugin` button.
   3. Fill in the information.
      - **Name** : Name of the plugin.
      - **Path** : Path to the plugin folder it is going to be saved.
      - **Tab List** : List to make a new widget/property.
        - **Name** : Name of the Widget/Property.
        - **Category** : Category of the Widget to be displayed and grouped in Editor Window.
        - **Type** : `Parameter`, `Folder`, `Property`.
      - **Enable Icon** : Enable Custom Icon that come with the plugin.
      
![Screenshot 2023-04-09 185256](https://user-images.githubusercontent.com/19835724/230806635-9244f3ea-98d8-4486-a0f7-cef463e393c6.png)

   4. Click `Create` button.

Once the plugin is created, it will be saved in the path you specified. The plugin will be loaded when you open the Layout Editor.</p>

 ### Manual
   1. Make new Dictionary in Plugins.
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
   3. Add Plugin Folder name to UIEditorProject.uiproject
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
    
  ### Ramp
    - Callback not implemented.
