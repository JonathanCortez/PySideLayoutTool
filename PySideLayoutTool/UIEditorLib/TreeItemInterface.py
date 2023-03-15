from PySide2 import QtCore, QtWidgets, QtGui
from abc import abstractmethod
from . import UIEditorMediators

""" 
(QtCore.Qt.ItemFlag) 
This enum describes the properties of an item:

Constant                    Description

Qt.NoItemFlags       -       It does not have any properties set.
Qt.ItemIsSelectable    -     It can be selected.
Qt.ItemIsEditable    -       It can be edited.
Qt.ItemIsDragEnabled    -    It can be dragged.
Qt.ItemIsDropEnabled    -    It can be used as a drop target.
Qt.ItemIsUserCheckable   -   It can be checked or unchecked by the user.
Qt.ItemIsEnabled     -       The user can interact with the item.

Qt.ItemIsAutoTristate   -    The item’s state depends on the state of its children. 
                            This enables automatic management of the state of parent items
                            in QTreeWidget (checked if all children are checked, unchecked 
                            if all children are unchecked, or partially checked if only some children are checked).

Qt.ItemIsTristate    -      This enum value is deprecated. Use instead.
Qt.ItemNeverHasChildren   - The item never has child items. This is used for optimization purposes only.
Qt.ItemIsUserTristate    -  The user can cycle through three separate states. This value was added in Qt 5.5.

"""

class TreeItem(QtWidgets.QTreeWidgetItem, UIEditorMediators.BaseComponent):
    def __init__(self,parent):
        super(TreeItem, self).__init__(parent)
        self._itemIn = parent
        self._display_index = -1
        self.setText(0, 'None')
        self._item_name = ''
        self._item_label = ''
        self._type = None


    def itemParent(self):
        return self._itemIn

    def setItem(self, item_In):
        if item_In.bOnItem():
            self._itemIn = item_In
        else:
            self._itemIn = item_In.itemParent()

        # print('parent : ', self._itemIn)

    def updateItem(self):
        self.setText(0, f'{self._item_label}({self._item_name})')

    def name(self):
        return self._item_name

    def setName(self, name: str):
        self._item_name = name
        self.updateItem()

    def label(self):
        return self._item_label

    def setLabel(self, label_str: str):
        self._item_label = label_str
        self.updateItem()
        self.mediator.notify_display_label(label_str)

    @property
    def stackIndex(self) -> int:
        return self._display_index

    @stackIndex.setter
    def stackIndex(self, index: int):
        self._display_index = index

    @property
    def type_str(self) -> str:
        return self._type

    @type_str.setter
    def type_str(self, type: str):
        self._type = type

    @abstractmethod
    def bMoveable(self) -> bool:
        """ Allow item to be move around layout tree items."""
        return True

    @abstractmethod
    def bOnItem(self) -> bool:
        """ Allow item to have children items. """
        return True

    @abstractmethod
    def itemHandling(self,item_adding, position):
        """ Override this method to handle how item is going to
            be added and moved in the layout tree.

            :param item_adding: new item being added to a QTreeWidgetItem or self.
            :param position: the last position item was dropped on.

        """



class RootItem(TreeItem):
    def __init__(self,parent):
        super(RootItem, self).__init__(parent)
        self.setText(0,'Root')
        self._font = QtGui.QFont()
        self._font.setBold(True)
        self.setFont(0, self._font)
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled)

    def setItem(self, item_In):
        pass

    def bMoveable(self) -> bool:
        return False

    def itemHandling(self,item_adding, position):
        if not isinstance(item_adding, QtWidgets.QTreeWidget):
            self.addChild(item_adding)




class ParmItem(TreeItem):
    def __init__(self):
        super(ParmItem, self).__init__(None)

    def bOnItem(self) -> bool:
        return False

    def itemHandling(self, item_adding, position):
        index = self.itemParent().indexOfChild(self)
        if position == QtWidgets.QAbstractItemView.BelowItem:
            index += 1

        self.itemParent().insertChild(index, item_adding)




class FolderItem(TreeItem):
    def __init__(self):
        super(FolderItem, self).__init__(None)
        self._font = QtGui.QFont()
        self._font.setItalic(True)
        self.setFont(0, self._font)

    def itemHandling(self, item_adding, position):
        if position == QtWidgets.QAbstractItemView.AboveItem:
            index = self.itemParent().indexOfChild(self)
            self.itemParent().insertChild(index, item_adding)
            return

        self.addChild(item_adding)




