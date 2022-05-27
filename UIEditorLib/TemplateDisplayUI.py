from PySide2 import QtCore, QtWidgets

from . import StringValidatorClass as Validator, UIEditorMediators
from ..UIEditorTemplates.Common.SeparatorTemplate import SeparatorWidgetClass
from ..UIEditorTemplates.Folder.CollapisbleFolderTemplate import CollapisbleFolderWidgetClass
from ..UIEditorTemplates.Layout import CustomFormLayout
from typing import Dict, Any, List


class RootUISetup(QtWidgets.QWidget):
    """ This class is parent to all other item in the tree for Parameter layout """
    def __init__(self, parent):
        super(RootUISetup, self).__init__()
        self._parent = parent

        layout = QtWidgets.QFormLayout()
        # layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        layout.setHorizontalSpacing(20)

        self._rest_button = QtWidgets.QPushButton('Rest')
        layout.addRow("Reset Layout:", self._rest_button)

        self.setLayout(layout)

        self._rest_button.pressed.connect(self._clear_tree)

    def nameState(self) -> bool:
        return True

    def _clear_tree(self):
        self._parent.clear_layout()



class ItemDisplayUI(QtWidgets.QWidget, UIEditorMediators.BaseComponent):

    def __init__(self):
        super(ItemDisplayUI, self).__init__()

        self._category_widgets: Dict[str, QtWidgets.QWidget] = {}
        self._category_layout: Dict[str, QtWidgets.QLayout] = {}
        self._category_open: Dict[str, bool] = {}

        self._widget_data: Dict[str, QtWidgets.QWidget] = {}
        self._layout_list_widgets: Dict[Any,List[Any]] = {}
        self._widget_label_data: Dict[str, QtWidgets.QWidget] = {}

        self._name_checked: bool = True
        self._type = ''

        self._mainLayout = QtWidgets.QVBoxLayout()
        self._mainLayout.setAlignment(QtCore.Qt.AlignTop)

        self.setLayout(self._mainLayout)


    def construct_display(self, instances, *args):
        for i in instances:
            current_layout = None
            if i.category in self._category_layout:
                current_layout = self._category_layout[i.category]
                list_widget = self._layout_list_widgets.pop(current_layout)
                list_widget.append(i.property_widget)
                layout_item = current_layout.new_Row(i.label,None, i.property_widget)
                self._widget_label_data[i.label] = layout_item.itemAt(0).widget()

                # self._category_layout[i.category] = current_layout
                self._layout_list_widgets[current_layout] = list_widget

            else:
                # names = i.category.split('|') #TODO: Handle sub category

                # self._mainLayout.addWidget(current_catergory_folder)
                # self._mainLayout.addSpacing(5)
                #
                # self._category_widgets[i.category] = current_catergory_folder
                current_layout = CustomFormLayout.CustomForm()
                new_list = [i.property_widget]
                self._layout_list_widgets[current_layout] = new_list
                self._category_layout[i.category] = current_layout
                layout_item = current_layout.new_Row(i.label,'None', i.property_widget)
                self._widget_label_data[i.label] = layout_item.itemAt(0).widget()

            # i.property_widget.addParent(current_catergory_folder)

            # Separator handling layout
            if i.separator:
                sep_widget = SeparatorWidgetClass.SeparatorHWidget()
                current_layout.add_Custom(sep_widget)

            if i.category_args[0]:
                self._category_open[i.category] = i.category_args[0]

            if i.label in self._widget_data:
                new_label = Validator.check_names(i.label, self._widget_data)
                self._widget_data[new_label] = i.property_widget
            else:
                self._widget_data[i.label] = i.property_widget

            if i.label == 'Name':
                i.property_widget._textbox._str_widget.editingFinished.connect(self.mediatorName)
                i.property_widget._textbox._str_widget.returnPressed.connect(self.mediatorNameCheck)

            if i.label == 'Label':
                i.property_widget._textbox._str_widget.editingFinished.connect(self.mediatorLabel)

            if i.label == 'Type':
                i.property_widget.setItems(args[0])
                i.property_widget.setCurrentItem(args[1])
                i.property_widget.propertyWidget().activated.connect(self._changeType)
                self._type = args[1]


        for key in self._category_layout:
            widget_layout = self._category_layout[key]
            state = False
            if key in self._category_open:
                state = True

            current_catergory_folder = CollapisbleFolderWidgetClass.CollapsibleFolderWidget(widget_layout)
            current_catergory_folder.folder_title(key)
            current_catergory_folder.open_folder(state)

            self._mainLayout.addWidget(current_catergory_folder)
            self._mainLayout.addSpacing(5)
            self._category_widgets[key] = current_catergory_folder

        # for key in self._category_widgets:
        #     widget_layout = self._category_layout[key]
        #     state = False
        #     if key in self._category_open:
        #         state = True
        #
        #     self._category_widgets[key].setContentLayout(widget_layout.layout(), state)


    def mediatorName(self):
        widget, label = self.findProperty('Name')
        self.mediator.update_item_name(widget.strText) #type: ignore
        self.setFocus()
        self._name_checked = False

    def mediatorNameCheck(self):
        widget, label = self.findProperty('Name')
        widget.setText(self.mediator.verifyName(widget.strText)) #type: ignore
        self.mediator.update_item_name(widget.strText) #type: ignore
        self._name_checked = True


    def mediatorLabel(self):
        widget, label = self.findProperty('Label')
        self.mediator.notify_item_label(widget.strText) #type: ignore
        self.setFocus()

    def nameState(self) -> bool:
        """ If name has been checked already """
        return self._name_checked

    def _changeType(self, arg__1):
        widget, label = self.findProperty('Type')
        text = widget.propertyWidget().itemText(arg__1)
        if text != self._type:
            self.mediator.updateChange(text) #type: ignore


    def findProperty(self, name: str):
        if name not in self._widget_data:
            AttributeError(f'{name} not in Display UI or has another name')
        else:
            return self._widget_data[name], self._widget_label_data[name]

    def type(self):
        return self._type

    def Properties(self):
        return self._widget_data
