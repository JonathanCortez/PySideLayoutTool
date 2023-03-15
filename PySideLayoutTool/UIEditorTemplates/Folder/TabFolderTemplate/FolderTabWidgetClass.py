from PySide2 import QtWidgets, QtCore


class TabWidgets(QtWidgets.QWidget):

    def __init__(self):
        super(TabWidgets,self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.setAlignment(QtCore.Qt.AlignTop)

        self.setLayout(self._layout)

    def addWidget(self, widget):
        self._layout.addWidget(widget)


class FolderMultiTabWidget(QtWidgets.QWidget):

    def __init__(self,widget, parent=None):
        super(FolderMultiTabWidget, self).__init__(parent)
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0,0,0,0)
        self._parent = parent

        self._tabs_widget = {}
        self.last_widget_removed = None

        self._base_widget = widget
        self._tabCount = 0

        self._position_types = {
            0 : QtWidgets.QTabWidget.North,
            1 : QtWidgets.QTabWidget.West,
            2 : QtWidgets.QTabWidget.East
        }

        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.setProperty('class','layout_pane')
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Fixed)

        self.tabWidget.addTab(QtWidgets.QWidget(), '+')
        self.tabWidget.tabBar().tabButton(0, QtWidgets.QTabBar.RightSide).resize(0, 0)

        self.tabWidget.tabBar().setSelectionBehaviorOnRemove(QtWidgets.QTabBar.SelectLeftTab)

        self._layout.addWidget(self.tabWidget)
        self.setLayout(self._layout)

        self.tabWidget.tabBarClicked.connect(self.newTab)
        self.tabWidget.tabBar().tabCloseRequested.connect(self.closeTab) #type: ignore


    def newTab(self, index):
        if self.tabWidget.tabText(index) == "+":
            self.insert_tab(index)

    def closeTab(self, index):
        self.last_widget_removed = self.tabWidget.widget(index)
        self.tabWidget.removeTab(index)
        self._tabCount -= 1
        del self._tabs_widget[f'{index+1}']

        if index < self._tabCount:
            for i in range(0, self._tabCount):
                self.tabWidget.setTabText(i,f'{i+1}')

    def insert_tab(self, index):
        new_widget = self._base_widget.clone(self, self._parent.layout_win(), False)
        self._tabs_widget[f'{index + 1}'] = new_widget
        self.tabWidget.insertTab(index, new_widget, f'{index + 1}')
        self._tabCount += 1

    def clear_tabwidget_data(self):
        self._tabs_widget.clear()
        self._tabCount = 0

    def set_base_widget(self, widget):
        self._base_widget = widget

    def setPlacement(self, index: int):
        self.tabWidget.setTabPosition(self._position_types[index])

    def currentIndex(self):
        return self.tabWidget.currentIndex()

    def count(self):
        return self._tabCount

    def tabContainer(self):
        return self._tabs_widget



class TabListButton(QtWidgets.QWidget):

    def __init__(self,parent, index):
        super(TabListButton, self).__init__()
        self._parent = parent
        self._index = index

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setAlignment(QtCore.Qt.AlignTop)

        self._hor_layout = QtWidgets.QHBoxLayout()
        self._hor_layout.setSpacing(3)
        self._hor_layout.setContentsMargins(5, 5, 5, 5)

        self._remove_button = QtWidgets.QPushButton(text='X')
        self._remove_button.setProperty('class','red_press')
        self._remove_button.setMinimumWidth(30)
        self._remove_button.setMaximumWidth(30)

        self._insert_button = QtWidgets.QPushButton(text='<<')
        self._insert_button.setProperty('class', 'add_press')
        self._insert_button.setMinimumWidth(30)
        self._insert_button.setMaximumWidth(30)

        self._hor_layout.addWidget(self._remove_button)
        self._hor_layout.addWidget(self._insert_button)

        self._layout.addLayout(self._hor_layout)

        self.setLayout(self._layout)

        self._remove_button.clicked.connect(self.removeWidget)
        self._insert_button.clicked.connect(self.insertWidget)

    def removeWidget(self, state):
        self._parent.removeWidget(self._index)

    def insertWidget(self, state):
        self._parent.insertWidget(self._index)

    def updateIndex(self,index):
        self._index = index

    def index(self):
        return self._index


class FolderMultiTabList(QtWidgets.QWidget):

    def __init__(self, widget, use_scroll_area=False, parent=None):
        super(FolderMultiTabList, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.setAlignment(QtCore.Qt.AlignTop)

        self._parent = parent

        self._hor_layout = QtWidgets.QHBoxLayout()
        self._hor_layout.setSpacing(5)
        self._hor_layout.setContentsMargins(0, 0, 0, 0)

        self._frame_layout = QtWidgets.QVBoxLayout()
        self._frame_layout.setSpacing(0)
        self._frame_layout.setContentsMargins(0,0,0,0)
        self._frame_layout.setAlignment(QtCore.Qt.AlignTop)

        self._folder_contents = []
        self._contents_button = []

        self.last_widget_removed = None
        self._base_widget = widget
        self._count = 0

        self._label = QtWidgets.QLabel()
        self._label.setMinimumWidth(65)
        self._label.setMaximumWidth(65)

        self._textbox = QtWidgets.QLineEdit()
        self._textbox.setText('0')
        self._textbox.setMinimumHeight(22)
        self._textbox.setMaximumHeight(22)

        self._addButton = QtWidgets.QPushButton(text='+')
        self._addButton.setMinimumWidth(25)
        self._addButton.setMaximumWidth(25)

        self._subButton = QtWidgets.QPushButton(text='-')
        self._subButton.setMinimumWidth(25)
        self._subButton.setMaximumWidth(25)

        self._clearButton = QtWidgets.QPushButton(text='clear')
        self._clearButton.setMinimumWidth(60)
        self._clearButton.setMaximumWidth(60)

        self._frame = QtWidgets.QGroupBox()
        self._frame.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Fixed)

        self._hor_layout.addSpacing(60)
        self._hor_layout.addWidget(self._label)
        self._hor_layout.addWidget(self._textbox)
        self._hor_layout.addWidget(self._addButton)
        self._hor_layout.addWidget(self._subButton)
        self._hor_layout.addWidget(self._clearButton)
        self._hor_layout.addSpacing(60)

        self._frame.setLayout(self._frame_layout)
        self._layout.addLayout(self._hor_layout)

        self._scroll_area = None

        if use_scroll_area:
            self._scroll_area = QtWidgets.QScrollArea()
            self._scroll_area.setWidgetResizable(True)
            self._scroll_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
            self._scroll_area.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

            self._scroll_area.setWidget(self._frame)
            self._layout.addWidget(self._scroll_area)

        else:
            self._layout.addWidget(self._frame)

        self.setLayout(self._layout)

        self._addButton.clicked.connect(self.new_widget)
        self._subButton.clicked.connect(self.removeWidget)
        self._clearButton.clicked.connect(self.clearWidgets)


    def new_widget(self):
        new_widget = self._base_widget.clone(self,self._parent.layout_win(),False)

        hor_layout = QtWidgets.QHBoxLayout()
        hor_layout.setSpacing(0)
        hor_layout.setContentsMargins(0, 0, 0, 0)

        widget_buttons = TabListButton(self, self._count)
        hor_layout.addWidget(widget_buttons)
        hor_layout.addWidget(new_widget)
        self._frame_layout.addLayout(hor_layout)
        self._count += 1

        self._textbox.setText(str(self._count))
        self._folder_contents.append(new_widget)
        self._contents_button.append(widget_buttons)

    def removeWidget(self, index):
        if type(index) == bool:
            index = self._count-1

        buttons = self._contents_button.pop(index)
        widget = self._folder_contents.pop(index)
        self.last_widget_removed = widget

        layout_item = self._frame_layout.itemAt(index)
        widget_button = layout_item.layout().itemAt(0).widget()
        widget_layout = layout_item.layout().itemAt(1).widget()
        widget_button.deleteLater()
        widget_layout.deleteLater()

        layout_item = self._frame_layout.itemAt(index)
        self._frame_layout.removeItem(layout_item)
        del widget, buttons, layout_item
        self._count -= 1
        self._textbox.setText(str(self._count))

        self.updateIndexs()

    def insertWidget(self, index):
        new_widget = self._base_widget.clone(self, self._parent.layout_win(), False)

        hor_layout = QtWidgets.QHBoxLayout()
        hor_layout.setSpacing(0)
        hor_layout.setContentsMargins(0, 0, 0, 0)

        widget_buttons = TabListButton(self, index)
        hor_layout.addWidget(widget_buttons)
        hor_layout.addWidget(new_widget)
        self._frame_layout.insertLayout(index,hor_layout)
        self._count += 1
        self._textbox.setText(str(self._count))
        self._folder_contents.insert(index,new_widget)
        self._contents_button.insert(index,widget_buttons)

        self.updateIndexs()


    def clearWidgets(self):
        current_count = self._frame_layout.count()

        for i in range(0,current_count):
            layout_item = self._frame_layout.itemAt(i)
            widget_button = layout_item.layout().itemAt(0).widget()
            widget_layout = layout_item.layout().itemAt(1).widget()
            widget_button.deleteLater()
            widget_layout.deleteLater()

        for i in range(0, current_count):
            layout_item = self._frame_layout.itemAt(0)
            self._frame_layout.removeItem(layout_item)
            del layout_item

        self._contents_button.clear()
        self._folder_contents.clear()

        self._count = 0
        self._textbox.setText(str(self._count))

    def updateIndexs(self):
        for i in range(0,self._frame_layout.count()):
            item = self._frame_layout.itemAt(i)
            item.itemAt(0).widget().updateIndex(i)


    def setName(self, name_str: str):
        self._label.setText(name_str)

    def count(self):
        return self._count

    def set_base_widget(self,widget):
        self._base_widget = widget

    def add_button_widget(self):
        return self._addButton

    def remove_button_widget(self):
        return self._subButton



class FolderTabList(QtWidgets.QWidget):

    def __init__(self, parent, widget):
        super(FolderTabList, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 5, 0, 5)

        self._parent = parent
        self._base_widget = widget

        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.setProperty('class', 'layout_pane')
        self.tabWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.tabWidget.addTab(widget,parent.label())

        self._layout.addWidget(self.tabWidget)
        self.setLayout(self._layout)


    def newTab(self, widget, label: str):
        self.tabWidget.addTab(widget, label)