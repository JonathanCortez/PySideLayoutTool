from PySide2 import QtCore, QtWidgets, QtGui

from PySideLayoutTool.UIEditorLib import UIEditorFactory, TreeItemInterface, TemplateDisplayUI, UIEditorMediators, TemplateDataClass
from ..UIEditorTemplates.Common.SeparatorTemplate import SeparatorWidgetClass
from . import TabScript


#TODO:
# - Add Name check properly to system. --(Fixed)
# - item widgets arrange order. --(Fixed)
# - fix widget form layout to align properly. --(Fixed)
# - fix widget layout spacing to far apart. --(Fixed)
# - objects being removed properly and in order. --(Fixed)
# - Add the other common Folder types and Widget types. --(Added)
# - Able to add item under a folder, show indicator under folders. --(Fixed)
# - Fix properly parenting when adding item above a folder. --(Fixed)
# - Fix Collapsible Tab Size when reapplying. --(Fixed)
# - Fix Collapsible within another Collapsible.
# - Fix Remove objects properly. --(Fixed)
# - basic Text Editor. --(Added)


class EditorWindow(QtWidgets.QMainWindow, UIEditorMediators.BaseComponent):
    def __init__(self, ui_name : str, path_given : str, category_name : str,parent=None):
        super(EditorWindow, self).__init__(parent)
        self.setWindowTitle(f'{ui_name} Editor Window')
        size = QtCore.QSize(1100, 600)
        self.setMinimumSize(size)

        self._ID_name = ui_name
        self._path_given = path_given
        self._category = category_name

        self._data = TemplateDataClass.TemplateData(self)

        dockTabs = QtWidgets.QDockWidget(self)
        dockTabs.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)

        tabWidget = QtWidgets.QTabWidget()
        tabWidget.setProperty('class','editor_pane')

        self._parm_tab = ParameterTab(self)
        self._pyEditor = TabScript.ScriptTab(self)
        tabWidget.addTab(self._parm_tab, 'Layout')
        tabWidget.addTab(self._pyEditor, 'Script')

        button_widgets = ButtonWidgets(self)
        display_name_widget = PathDispaly(ui_name, path_given, category_name)

        combinedWidgets = CombineWidget(display_name_widget, tabWidget, button_widgets)

        dockTabs.setWidget(combinedWidgets)

        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dockTabs)

    def pyModules(self) -> int:
        return self._pyEditor.pyModules_count()

    def pyModule(self,name: str):
        return self._pyEditor.getPyModules().scriptModule(name).toPlainText()

    def pyEditor(self):
        return self._pyEditor

    def layout_win_obj(self):
        return self.mediator.layout_window() #type: ignore

    def TemplateLayout(self):
        return self._data

    def LayoutDisplay(self):
        self.mediator.notifyDisplay() #type: ignore

    def LayoutUpdate(self):
        self.mediator.notifyUpdate(self._data.newLayout(self.layout_win_obj())) #type: ignore

    def editor_name(self):
        return self._ID_name

    def editor_path(self):
        return self._path_given

    def editor_category(self):
        return self._category

    def parameter_Tab(self):
        return self._parm_tab

    def restoreUIState(self, data_passed):
        self.mediator.restoreWins(data_passed) #type: ignore

    def closeEvent(self, event) -> None:
        pass


class CombineWidget(QtWidgets.QWidget):
    def __init__(self,*args):
        super(CombineWidget, self).__init__()
        self._vertical_layout = QtWidgets.QVBoxLayout()
        self._vertical_layout.setAlignment(QtCore.Qt.AlignTop)
        self._vertical_layout.setContentsMargins(5, 5, 5, 5)

        for arg in args:
            self._vertical_layout.addWidget(arg)

        self.setLayout(self._vertical_layout)



class PathDispaly(QtWidgets.QWidget):
    def __init__(self, UI_name: str, path_str: str, category: str):
        super(PathDispaly, self).__init__()
        self._layout = QtWidgets.QFormLayout()

        hor_layout = QtWidgets.QHBoxLayout()

        self._ui_name = QtWidgets.QLabel(text=UI_name)
        self._category_name = QtWidgets.QLabel(text=category)
        self._ui_path = QtWidgets.QLineEdit(text=path_str)

        self._button = QtWidgets.QPushButton()
        self._file_dialog = QtWidgets.QFileDialog()

        hor_layout.addWidget(self._ui_path)
        hor_layout.addWidget(self._button)

        self._layout.addRow('UI Name :', self._ui_name)
        self._layout.addRow('Category :', self._category_name)
        self._layout.addRow('File Path :',hor_layout)

        self.setLayout(self._layout)




class ButtonWidgets(QtWidgets.QWidget):
    def __init__(self, parent):
        super(ButtonWidgets, self).__init__()
        self._main_win = parent
        self.setMinimumHeight(35)
        self.setMaximumHeight(35)

        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setAlignment(QtCore.Qt.AlignRight)
        self._layout.setContentsMargins(5, 5, 5, 5)

        self._view_button = QtWidgets.QPushButton(text='View')
        self._view_button.setProperty('class', 'button_width')

        self._apply_button = QtWidgets.QPushButton(text='Apply')
        self._apply_button.setProperty('class', 'button_width')

        self._discard_button = QtWidgets.QPushButton(text='Discard')
        self._discard_button.setProperty('class', 'button_width')

        self._accept_button = QtWidgets.QPushButton(text='Accept')
        self._cancel_button = QtWidgets.QPushButton(text='Cancel')

        self._layout.addWidget(self._view_button)
        self._layout.addSpacing(40)

        self._layout.addWidget(self._apply_button)
        self._layout.addSpacing(10)
        self._layout.addWidget(self._discard_button)
        self._layout.addSpacing(40)
        self._layout.addWidget(self._accept_button)
        self._layout.addSpacing(10)
        self._layout.addWidget(self._cancel_button)

        self.setLayout(self._layout)

        self._view_button.pressed.connect(self.viewLayout)
        self._apply_button.pressed.connect(self.updateWindowLayout)
        self._accept_button.pressed.connect(self.acceptFunc)
        self._cancel_button.pressed.connect(self.closeEditor)

    def viewLayout(self):
        self._main_win.LayoutDisplay()

    def updateWindowLayout(self):
        self._main_win.LayoutUpdate()

    def acceptFunc(self):
        self.updateWindowLayout()
        self.viewLayout()
        self._main_win.close()

    def closeEditor(self):
        self._main_win.close()


class ParameterTab(QtWidgets.QWidget):
    def __init__(self, main_parent):
        super(ParameterTab, self).__init__()
        self._window_parent = main_parent

        self._horizontal_layout = QtWidgets.QHBoxLayout()
        self._horizontal_layout.setAlignment(QtCore.Qt.AlignLeft)
        self._horizontal_layout.setSpacing(10)
        self._horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self._horizontal_layout.addWidget(ParameterList())

        self._displayWidget = ParameterDisplay(self)
        self._ItemLayout = LayoutTree(main_parent, self._displayWidget)

        self._splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self._splitter.setChildrenCollapsible(False)

        self._scrollArea = QtWidgets.QScrollArea()
        self._scrollArea.setWidgetResizable(True)
        self._scrollArea.setWidget(self._displayWidget)
        self._scrollArea.setStyleSheet("QScrollArea{ border: 0px;}")

        self._splitter.addWidget(self._ItemLayout)
        self._splitter.addWidget(self._scrollArea)

        self._horizontal_layout.addWidget(self._splitter)

        self.setLayout(self._horizontal_layout)

    def layout_tree(self):
        return self._ItemLayout



class ParameterDisplay(QtWidgets.QWidget):
    def __init__(self, parent):
        super(ParameterDisplay, self).__init__()
        self._parent = parent

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setAlignment(QtCore.Qt.AlignTop)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(5, 5, 5, 5)

        self._stack = QtWidgets.QStackedWidget(self)

        self._header = QtWidgets.QLabel('Description')
        self._header.setStyleSheet("QLabel{"
                                     " font-size: 16px;"
                                     " font-weight: bold;}")

        self._separator = SeparatorWidgetClass.SeparatorHWidget()

        self._layout.addWidget(self._header)
        self._layout.addWidget(self._separator)
        self._layout.addWidget(self._stack)

        self.setLayout(self._layout)


    def addStack(self, widget: QtWidgets.QWidget) -> int:
        return self._stack.addWidget(widget)

    def removeStack(self, widget: QtWidgets.QWidget) -> None:
        self._stack.removeWidget(widget)

    def findStack(self, widget :QtWidgets.QWidget) -> int:
        index = self._stack.indexOf(widget)
        if index == -1:
            index = self.addStack(widget)

        return index

    def widgetStack(self, index: int):
        return self._stack.widget(index)

    def displayCurrent(self, index: int) -> None:
        self._stack.setCurrentIndex(index)




class ParameterList(QtWidgets.QTreeWidget):
    def __init__(self):
        super(ParameterList, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.setHeaderLabel('Templates Supported')
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)

        registeredWidgets = UIEditorFactory.WidgetFactory.registered()
        for key in registeredWidgets:
            category_item = QtWidgets.QTreeWidgetItem(self)
            category_item.setText(0,key)
            category_item.setExpanded(True)
            category_item.setFlags(QtCore.Qt.ItemIsEnabled)
            for itemName in UIEditorFactory.WidgetFactory.sortCategoryItems(registeredWidgets[key]):
                item = QtWidgets.QTreeWidgetItem(category_item)
                item.setText(0, itemName)
                category_item.addChild(item)




    def startDrag(self, supportedActions) -> None:
        if self.selectedIndexes():
            selitem = self.selectedItems()[0]
            # main_catgory_str = self.selectedItems()[0].parent().text(0)
            selectedName = selitem.text(0)
            # textpassed = main_catgory_str + '.' + selectedName

            mimeData = QtCore.QMimeData()
            mimeData.setText(selectedName)
            drag = QtGui.QDrag(self)
            drag.setMimeData(mimeData)
            drag.exec_(supportedActions, QtCore.Qt.CopyAction)
            # pixmap = QtGui.QPixmap(self._labelTest.size())
            # self._labelTest.render(pixmap)
            # drag.setPixmap(pixmap)
            # dropAction = drag.start(QtCore.Qt.CopyAction)




class LayoutTree(QtWidgets.QTreeWidget):
    def __init__(self, parent, showWidget):
        super(LayoutTree, self).__init__()
        self.setDragDropMode(QtWidgets.QAbstractItemView.DropOnly and QtWidgets.QAbstractItemView.InternalMove)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self._parent = parent
        self.setHeaderLabel('Layout')
        self.dropIndicatorRect = QtCore.QRect()
        self._displayWidget = showWidget

        self._currentItem = None
        self._bisChild = True
        self._bSameItem = True
        self._rowOn = -1

        rootclass = TreeItemInterface.RootItem(self)
        rootclass._item_name = 'Root'
        self.addTopLevelItem(rootclass)
        self._root_item = self.topLevelItem(0)
        self._root_item.stackIndex = self._displayWidget.addStack(TemplateDisplayUI.RootUISetup(self))

        # self.selectionModel().selectionChanged.connect(self.handleSelection) #type: ignore
        self.itemPressed.connect(self.item_pressed)
        self.itemDoubleClicked.connect(self.item_name_change)


    # def handleSelection(self, selected, deselected):
    #     folder_items = []
    #     for index in selected.indexes():
    #         item = self.itemFromIndex(index)
    #         if isinstance(self.itemFromIndex(index), TreeItemInterface.FolderItem):
    #             folder_items.append(item)
    #
    #     # if folder_items:
    #     #     self.selectionModel().Current = folder_items




    def item_name_change(self, item, column):
        if item is not self._root_item:
            self.setItemWidget(item,0,ItemEditWidget(item.label(), item, self))


    def item_pressed(self, item, index):
        if self._currentItem is None:
            self._currentItem = item

        display_widget = self._displayWidget.widgetStack(self._currentItem.stackIndex)

        if self._currentItem != self._root_item:
            display_widget.mediatorNameCheck()

        self._currentItem = item
        self.setState(QtWidgets.QAbstractItemView.EditingState)
        self._displayWidget.displayCurrent(item.stackIndex)
        self.setState(QtWidgets.QAbstractItemView.NoState)



    def startDrag(self, supportedActions) -> None:
        listsQModelIndex = []
        for i in self.selectedIndexes():
            item = self.itemFromIndex(i)
            if item.bMoveable():
                listsQModelIndex.append(i)

        mimeData = QtCore.QMimeData()
        dataQMimeData = self.model().mimeData(listsQModelIndex)
        dragQDrag = QtGui.QDrag(self)
        # dragQDrag.setPixmap(QtGui.QPixmap('test.jpg')) # <- For put your custom image here
        dragQDrag.setMimeData(dataQMimeData)
        dragQDrag.exec_(supportedActions, QtCore.Qt.MoveAction)


        # listsQModelIndex = self.selectedIndexes()
        # if listsQModelIndex and self.selectedItems()[0].bMoveable():
        #     self._currentItem = self.selectedItems()[0]
        #     if self._currentItem.bMoveable():
        #         mimeData = QtCore.QMimeData()
        #         dataQMimeData = self.model().mimeData(listsQModelIndex)
        #         dragQDrag = QtGui.QDrag(self)
        #         # dragQDrag.setPixmap(QtGui.QPixmap('test.jpg')) # <- For put your custom image here
        #         dragQDrag.setMimeData(dataQMimeData)
        #         dragQDrag.exec_(supportedActions, QtCore.Qt.MoveAction)



    def keyPressEvent(self, event) -> None:
        if event.key() == QtCore.Qt.Key_Backspace or event.key() == QtCore.Qt.Key_Delete:
            for on_selection in self.selectedItems():
                if on_selection is not self._root_item:

                    if on_selection.childCount() > 0:
                        index = self.indexFromItem(on_selection).row()
                        for i in self._parent.TemplateLayout().item_groups()[on_selection.name()]:
                            on_selection.removeChild(i)
                            # on_selection.itemParent().itemHandling(i, None)
                            i.setItem(on_selection.itemParent())
                            on_selection.itemParent().insertChild(index, i)
                            index += 1

                    self.EditorWin().TemplateLayout().remove_data_obj(on_selection)
                    on_selection.itemParent().removeChild(on_selection)
                    display_widget = self._displayWidget.widgetStack(on_selection.stackIndex)
                    self._displayWidget.removeStack(display_widget)
                    self._update_display_item_index()
                    self._check_below_items()
                    itemdel = on_selection
                    self._currentItem = None
                    del itemdel, display_widget



    def dragEnterEvent(self, event) -> None:
        event.acceptProposedAction()
        if event.dropAction() != QtCore.Qt.MoveAction:
            self._currentItem = None


    def dragMoveEvent(self, event) -> None:
        pos = event.pos()
        item = self.itemAt(pos)
        self.setState(QtWidgets.QAbstractItemView.DraggingState)

        if item:
            index = self.indexFromItem(item)  # this always get the default 0 column index
            self._bSameItem = True if item is not self._currentItem else False
            self._rowOn = self.indexFromItem(item).row()
            self._bisChild = True

            if event.dropAction() == QtCore.Qt.MoveAction and self._currentItem.bOnItem() and self._bSameItem:
                if item is not self._root_item:
                    self._bisChild = self.isItemChild(item)

            rect = self.visualRect(index)
            rect_left = self.visualRect(index.sibling(index.row(), 0))
            rect_right = self.visualRect(index.sibling(index.row(), self.header().logicalIndex(self.columnCount() - 1)))  # in case section has been moved

            self.dropIndicatorPosition = self.position(event.pos(), rect)

            # print(f'under Folder: {self.isUnderFolder(item)}, Same Item: {self._bSameItem}')

            if self.dropIndicatorPosition == self.AboveItem and item is not self._root_item and self._bSameItem and self._bisChild and self.isUnderFolder(item):
                self.dropIndicatorRect = QtCore.QRect(rect_left.left(), rect_left.top(), rect_right.right() - rect_left.left(), 0)
                event.accept()
            elif self.dropIndicatorPosition == self.BelowItem and self._bSameItem and self.itemBelow(item) is not self._currentItem and self._bisChild and not item.bOnItem():
                self.dropIndicatorRect = QtCore.QRect(rect_left.left(), rect_left.bottom(), rect_right.right() - rect_left.left(), 0)
                event.accept()
            elif self.dropIndicatorPosition == self.OnItem and item.bOnItem() and self._bSameItem and self._bisChild:
                self.dropIndicatorRect = QtCore.QRect(rect_left.left(), rect_left.top(), rect_right.right() - rect_left.left(), rect.height())
                event.accept()
            else:
                self.dropIndicatorRect = QtCore.QRect()

            self.model().setData(index, self.dropIndicatorPosition, QtCore.Qt.UserRole)

        # This is necessary or else the previously drawn rect won't be erased
        self.viewport().update()


    def dropEvent(self, event) -> None:
        pos = event.pos()
        item = self.itemAt(pos)

        self.dropIndicatorPosition = self.position(event.pos(), self.visualRect(self.indexFromItem(item)))

        if self.dropIndicatorPosition == self.AboveItem and item == self._root_item:
            return

        if item is None:
            item = self._root_item

        if event.mimeData().hasFormat("text/plain"):
            passedData = event.mimeData().text()
            self.add_new_obj(passedData, item, self.dropIndicatorPosition)

            event.acceptProposedAction()
            self.setState(QtWidgets.QAbstractItemView.NoState)
            QtWidgets.QTreeWidget.dropEvent(self, event)
            self.setExpanded(self.indexFromItem(item), True)

        # TODO: Just for looks, update treeWidget highlight mark when item gets added or moved.

        if event.dropAction() == QtCore.Qt.MoveAction and self._bSameItem and item.itemParent() is not self._currentItem and self._bisChild:
            selected_items = []
            for on_selection in self.selectedItems():
                if isinstance(on_selection , TreeItemInterface.FolderItem):
                    if not isinstance(on_selection.itemParent(), TreeItemInterface.FolderItem):
                        selected_items.append(on_selection)

                    elif item != on_selection.itemParent():
                        selected_items.append(on_selection)

                elif item != on_selection.itemParent():
                    selected_items.append(on_selection)

            remove_selections = []
            for selection in selected_items:
                if selection.itemParent() in selected_items:
                    remove_selections.append(selection)

            for r in remove_selections:
                selected_items.remove(r)

            for i in selected_items:
                i.itemParent().removeChild(i)
                item.itemHandling(i, self.dropIndicatorPosition)
                self.setExpanded(self.indexFromItem(item), True)
                self.setExpanded(self.indexFromItem(i), True)
                self.parent_handling(i, item)
                self.EditorWin().TemplateLayout().update_groups(i, self.indexFromItem(i).row())
            # TODO: still keep an eye on parenting when moved if it works property throughout the application growth

        self._check_below_items()




    def isItemChild(self, item) -> bool:
        parent_On = self.itemFromIndex(self.indexFromItem(item).parent())
        state = True
        if parent_On is self._root_item:
            state = True

        elif parent_On is not self._currentItem:
            state = self.isItemChild(parent_On)
        else:
            state = False

        return state


    def parent_handling(self,current_item, item_on: QtWidgets.QTreeWidgetItem):
        if self.dropIndicatorPosition == self.AboveItem and item_on.bOnItem():
            current_item.setItem(item_on.itemParent())
        else:
            current_item.setItem(item_on)


    def isUnderFolder(self, item):
        model_index = self.indexFromItem(item)
        if model_index.row() == 0:
            return True
        else:
            above_model = model_index.sibling(model_index.row()-1,0)
            above_item = self.itemFromIndex(above_model)
            return above_item.bOnItem()



    def position(self, pos, rect):
        rec = QtWidgets.QAbstractItemView.OnViewport

        # margin*2 must be smaller than row height, or the drop onItem rect won't show
        margin = 5
        if pos.y() - rect.top() < margin:
            rec = QtWidgets.QAbstractItemView.AboveItem
        elif rect.bottom() - pos.y() < margin:
            rec = QtWidgets.QAbstractItemView.BelowItem

        elif pos.y() - rect.top() > margin and rect.bottom() - pos.y() > margin:
            rec = QtWidgets.QAbstractItemView.OnItem

        return rec

    def paintEvent(self, event):
        painter = QtGui.QPainter(self.viewport())
        self.drawTree(painter, event.region())
        # in original implementation, it calls an inline function paintDropIndicator here
        self.paintDropIndicator(painter)



    def paintDropIndicator(self, painter):
        if self.state() == QtWidgets.QAbstractItemView.DraggingState:
            opt = QtWidgets.QStyleOption()
            opt.init(self)
            opt.rect = self.dropIndicatorRect
            rect = opt.rect

            brush = QtGui.QBrush(QtGui.QColor(QtCore.Qt.gray))

            if rect.height() == 0:
                pen = QtGui.QPen(brush, 2, QtCore.Qt.SolidLine)
                painter.setPen(pen)
                painter.drawLine(rect.topLeft(), rect.topRight())
            else:
                pen = QtGui.QPen(brush, 2, QtCore.Qt.SolidLine)
                painter.setPen(pen)
                painter.drawRect(rect)

    def set_current_objects(self, item : QtWidgets.QTreeWidgetItem, widget: QtWidgets.QWidget, display):
        self._currentItem = item
        string_type = item.type_str

        #TODO: Handle how Folderlist is parented must be refactored.
        if isinstance(item, TreeItemInterface.FolderItem):
            if widget.bisFolderList():
                other_name = ''
                if self.isUnderFolder(item):
                    if self.itemBelow(item) == self._root_item and self.indexFromItem(item).row() == 0:
                        other_name = 'Root'
                    elif isinstance(self.itemAbove(item), TreeItemInterface.FolderItem):
                        other_name = self.itemAbove(item).name()
                    else:
                        model_index = self.indexFromItem(item)
                        other_name = self.itemFromIndex(model_index.sibling(model_index.row()-1,0)).name()
                else:
                    other_name = 'Root'

                self.EditorWin().TemplateLayout().add_folderlist_data(item.name(), widget, other_name)

        self.EditorWin().TemplateLayout().layout_names()[item] = item.name()
        self.EditorWin().TemplateLayout().add_group_data(item, widget,display, string_type, self.indexFromItem(item).row())


    def _update_display_item_index(self):
        items = self.EditorWin().TemplateLayout().item_groups()
        for key in self.EditorWin().TemplateLayout().display_groups():
            for itr in enumerate(self.EditorWin().TemplateLayout().display_groups()[key]):
                index = self._displayWidget.findStack(itr[1])
                item = items[key][itr[0]]
                item.stackIndex = index

    #Sets item display properties to be disable/enable
    def _check_below_items(self):
        data = self.EditorWin().TemplateLayout()
        items = data.item_groups()

        for key in items:
            for i in items[key]:
                if not i.bOnItem():
                    item_below = self.itemBelow(i)
                    widget_property, label_widget = self._displayWidget.widgetStack(i.stackIndex).findProperty('Horizontal join')
                    if item_below:
                        if item_below.itemParent() == i.itemParent() and item_below.bOnItem():
                            widget_property.setValue(False)
                            widget_property.setDisabled(True)
                            label_widget.setDisabled(True)

                        elif item_below.itemParent() != i.itemParent():
                            widget_property.setValue(False)
                            widget_property.setDisabled(True)
                            label_widget.setDisabled(True)

                        else:
                            widget_property.setDisabled(False)
                            label_widget.setDisabled(False)

                    else:
                        widget_property.setValue(False)
                        widget_property.setDisabled(True)
                        label_widget.setDisabled(True)



    def add_new_obj(self,  string_type: str, item_on: QtWidgets.QTreeWidgetItem, position_on):
        category_in = UIEditorFactory.WidgetFactory.ItemCategoryIn(string_type)
        build_class = UIEditorFactory.WidgetFactory.create(string_type)
        build_class.InitObjects()
        build_class.FillObjects(category_in, string_type)
        build_class.Item_management(item_on, position_on)
        build_class.Database_Fill(self)
        return build_class

    def itemHandling(self,new_item, position):
        self.addTopLevelItem(new_item)

    def EditorWin(self):
        return self._parent

    def layoutWin(self):
        return self._parent.layout_win_obj()

    def displayObject(self):
        return self._displayWidget

    def root_item(self):
        return self._root_item

    def clear_layout(self):
        for key in self.EditorWin().TemplateLayout().item_groups():
            for item in self.EditorWin().TemplateLayout().item_groups()[key]:
                self._root_item.removeChild(item)

        self.EditorWin().TemplateLayout().clear_data()



class ItemEditWidget(QtWidgets.QLineEdit):
    def __init__(self, text, item, tree):
        super(ItemEditWidget, self).__init__()
        self.setFixedSize(150,17)

        self._current_text = text
        self._currentItem = item
        self._currentTree = tree
        self.setText(text)

        self.setStyleSheet(
        "border-radius: 2px;"
        )

        self.editingFinished.connect(self.edited)

    def edited(self):
        current_text = self.text()

        if current_text is not'':
            if current_text is not self._current_text:
                self._current_text = current_text
                self._currentItem.setLabel(current_text)

        self._currentTree.setItemWidget(self._currentItem,0,None)




