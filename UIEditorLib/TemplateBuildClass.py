from abc import ABC, abstractmethod

from PySide2 import QtWidgets, QtGui
from . import TemplateDisplayUI, TreeItemInterface, UIEditorMediators, StringValidatorClass, UIEditorIconFactory, \
    UIEditorFactory


class TemplateBuilderInterface(ABC):

    @abstractmethod
    def InitObjects(self):
        """ Initialize Objects that need to be handled."""

    @abstractmethod
    def FillObjects(self, *args):
        """ something """

    @abstractmethod
    def Item_management(self, item_on, position):
        """...."""

    @abstractmethod
    def Database_Fill(self, parent_tree):
        """..."""

    @abstractmethod
    def prefixStart_name(self) -> str:
        """ Name to start off """

    @abstractmethod
    def prefixStart_label(self) -> str:
        """ Label to start off"""

    @abstractmethod
    def set_icon(self) -> None:
        """ Set a custom Icon that is registered."""

    @abstractmethod
    def itemTreeClass(self) -> TreeItemInterface.TreeItem:
        """ Implement how tree item is handled when on current item"""

    @abstractmethod
    def widgetClass(self):
        """ widget"""



class BaseConcreteBuilder(TemplateBuilderInterface):

    def __init__(self):
        self._new_widget = None
        self._new_item = None
        self._new_display = None
        self._mediator = None

        self.__instances = None


    def newItem(self):
        return self._new_item

    def newWidget(self):
        return self._new_widget

    def newDisplay(self):
        return self._new_display


    def InitObjects(self):
        self._new_widget = self.widgetClass()
        self._new_display = TemplateDisplayUI.ItemDisplayUI()
        self._new_item = self.itemTreeClass()
        self._mediator = UIEditorMediators.LayoutMediator(self._new_item, self._new_display)

    def FillObjects(self, *args):
        self.__instances = self._new_widget._displayProperties()
        registered_widgets = UIEditorFactory.WidgetFactory.registered()
        sorted_list = UIEditorFactory.WidgetFactory.sortCategoryItems(registered_widgets[args[0]])
        self._new_display.construct_display(self.__instances, sorted_list, args[1])

        self._new_item.type_str = args[1]
        if self.set_icon() is not None:
            icon = QtGui.QIcon(self.set_icon()) #type: ignore
            self._new_item.setIcon(0,self.set_icon())


    def Item_management(self, item_on, position):
        if position == QtWidgets.QAbstractItemView.AboveItem and item_on.bOnItem():
            self._new_item.setItem(item_on.itemParent())
        else:
            self._new_item.setItem(item_on)

        item_on.itemHandling(self._new_item, position)


    def Item_management_index(self, item_on, index):
        item_parent = item_on.itemParent()
        self._new_item.setItem(item_parent)
        item_parent.insertChild(index,self._new_item)


    def Database_Fill(self, parent_tree):
        new_widget = self._new_widget(None)
        new_widget._pass_instances(self.__instances)
        self._new_widget = new_widget

        self._new_item.stackIndex = parent_tree.displayObject().addStack(self._new_display)
        parent_tree.displayObject().displayCurrent(self._new_item.stackIndex)
        self._mediator.notifyAll(
            name=StringValidatorClass.checkString(StringValidatorClass.check_prefix_name(self.prefixStart_name())),
            label=self.prefixStart_label())
        parent_tree.set_current_objects(self._new_item, self._new_widget, self._new_display)


    def clone_widget(self, widget_cloning):
        self._new_widget = self.widgetClass()
        instances = self._new_widget._displayProperties()

        for i in instances:
            clone_value = widget_cloning.__property_instances__[i.func_owner].value()
            if i.func_owner == 'name':
                clone_value = clone_value + '_1'
                # print(clone_value)

            i.property_widget.setValue(clone_value)

        new_widget = self._new_widget(None)
        new_widget._pass_instances(instances)
        self._new_widget = new_widget



    @abstractmethod
    def prefixStart_name(self) -> str:
        """ Name to start off """

    @abstractmethod
    def prefixStart_label(self) -> str:
        """ Label to start off"""

    @abstractmethod
    def set_icon(self) -> None:
        """ Set a custom Icon that is registered."""

    @abstractmethod
    def itemTreeClass(self) -> TreeItemInterface.TreeItem:
        """ Implement how tree item is handled when on current item"""

    @abstractmethod
    def widgetClass(self):
        """ widget"""



class BaseTemplateBuildClass(ABC):

    def construct(self, item_On, position, parent_tree, type_strings):
        new_widget_class = self.widgetClass()
        new_display = TemplateDisplayUI.ItemDisplayUI()
        instances = new_widget_class._displayProperties()
        registeredWidgets = UIEditorFactory.WidgetFactory.registered()
        sorted_list = UIEditorFactory.WidgetFactory.sortCategoryItems(registeredWidgets[type_strings[0]])
        new_display.construct_display(instances,sorted_list , type_strings[1])
        new_widget = new_widget_class()
        new_widget._pass_instances(instances)

        new_item = self.itemTreeClass()
        mediator = UIEditorMediators.LayoutMediator(new_item, new_display)

        if self.set_icon() is not None:
            icon = QtGui.QIcon(self.set_icon()) #type: ignore
            new_item.setIcon(0,icon)

        if position == QtWidgets.QAbstractItemView.AboveItem and item_On.bOnItem():
            new_item.setItem(item_On.itemParent())
        else:
            new_item.setItem(item_On)

        new_item.stackIndex = parent_tree.displayObject().addStack(new_display)
        item_On.itemHandling(new_item, position)
        parent_tree.displayObject().displayCurrent(new_item.stackIndex)
        mediator.notifyAll(name=StringValidatorClass.checkString(
            StringValidatorClass.check_prefix_name(self.prefixStart_name())),
                           label=self.prefixStart_label())
        parent_tree.set_current_objects(new_item, new_widget)



    @abstractmethod
    def prefixStart_name(self) -> str:
        """ Name to start off """

    @abstractmethod
    def prefixStart_label(self) -> str:
        """ Label to start off"""

    @abstractmethod
    def set_icon(self) -> None:
        """ Set a custom Icon that is registered."""

    @abstractmethod
    def itemTreeClass(self) -> TreeItemInterface.TreeItem:
        """ Implement how tree item is handled when on current item"""

    @abstractmethod
    def widgetClass(self):
        """ widget"""




class RootBuild(BaseConcreteBuilder):
    """ This Class should not be inherit or modified, unless
        you know the framework of this application.
    """
    def prefixStart_name(self) -> str:
        return 'root'

    def prefixStart_label(self) -> str:
        return 'Root'

    def set_icon(self) -> None:
        pass



class ParameterBuild(BaseConcreteBuilder):

    def prefixStart_name(self) -> str:
        return 'newparameter'

    def prefixStart_label(self) -> str:
        return 'Label'

    def itemTreeClass(self) -> TreeItemInterface.TreeItem:
        return TreeItemInterface.ParmItem()

    def set_icon(self) -> None:
        return None



class FolderBuild(BaseConcreteBuilder):

    def prefixStart_name(self) -> str:
        return 'newfolder'

    def prefixStart_label(self) -> str:
        return 'FolderLabel'

    def itemTreeClass(self) -> TreeItemInterface.TreeItem:
        return TreeItemInterface.FolderItem()

    def set_icon(self) -> None:
        return UIEditorIconFactory.IconEditorFactory.create('folder_nor')

