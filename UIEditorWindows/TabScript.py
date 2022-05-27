from PySide2 import QtWidgets, QtCore, QtGui

from PySideLayoutTool.UIEditorLib import UIEditorIconFactory, UIEditorScript


class ScriptTab(QtWidgets.QMainWindow):

    def __init__(self, parent):
        super(ScriptTab, self).__init__()
        self._parent = parent
        self._editor_dock = QtWidgets.QDockWidget(self)
        self._editor_dock.setWindowTitle('Python Editor')
        self._editor_dock.setAllowedAreas(QtCore.Qt.TopDockWidgetArea)

        self._editor_layout = EditorLayout()
        self._editor_dock.setWidget(self._editor_layout)
        self._editor_dock.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable | QtWidgets.QDockWidget.DockWidgetMovable)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea,self._editor_dock)

    def getPyModules(self):
        return self._editor_layout

    def pyModules_count(self):
        return self._editor_layout.module_count()

    def pyModule_editor(self):
        return self._editor_layout


class EditorLayout(QtWidgets.QWidget):

    def __init__(self):
        super(EditorLayout, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0,0,0,0)

        self._top_toolbar = QtWidgets.QToolBar()
        self._bottom_toolbar = QtWidgets.QToolBar()
        self._pyModules = {}

        self._left_move_action = self._top_toolbar.addAction(UIEditorIconFactory.IconEditorFactory.create('move_left'), 'Line Left Move')
        self._right_move_action = self._top_toolbar.addAction(UIEditorIconFactory.IconEditorFactory.create('move_right'), 'Line Right Move')

        self._top_toolbar.addSeparator()

        self._comment_action = self._top_toolbar.addAction(UIEditorIconFactory.IconEditorFactory.create('comment'), 'Comment In/Out')
        self._top_toolbar.addSeparator()

        spacing = QtWidgets.QWidget()
        spacing.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        spacing.setStyleSheet('background-color: #0e0e0e;')

        self._bottom_toolbar.addWidget(spacing)
        self._bottom_toolbar.addSeparator()
        self._zoom_in_action = self._bottom_toolbar.addAction(UIEditorIconFactory.IconEditorFactory.create('zoom_In'), 'Increase Text Size')
        self._zoom_out_action = self._bottom_toolbar.addAction(UIEditorIconFactory.IconEditorFactory.create('zoom_Out'), 'Decrease Text Size')

        self._tab_widget = QtWidgets.QTabWidget(self)
        self._tab_widget.setProperty('class','editor_pane')
        self._tab_widget.setTabsClosable(True)

        self._base_pyModule = UIEditorScript.ScriptEditor()
        self._tab_widget.addTab(self._base_pyModule,'PyModule_1')
        self._tab_widget.tabBar().tabButton(0,QtWidgets.QTabBar.RightSide).resize(0, 0)
        self._pyModules['PyModule_1'] = self._base_pyModule

        self._tab_widget.addTab(QtWidgets.QWidget(), '+' )
        self._tab_widget.tabBar().tabButton(1, QtWidgets.QTabBar.RightSide).resize(0, 0)

        self._tab_widget.tabBar().setSelectionBehaviorOnRemove(QtWidgets.QTabBar.SelectLeftTab)

        self._layout.addWidget(self._top_toolbar)
        self._layout.addWidget(self._tab_widget)
        self._layout.addWidget(self._bottom_toolbar)

        self._left_move_action.triggered.connect(self.move_line_back)
        self._right_move_action.triggered.connect(self.move_line_forward)
        self._comment_action.triggered.connect(self.comment_action)

        self._zoom_in_action.triggered.connect(self.zoom_in_call)
        self._zoom_out_action.triggered.connect(self.zoom_out_call)

        self._tab_widget.tabBarClicked.connect(self.newTab)
        self._tab_widget.tabBar().tabCloseRequested.connect(self.closeTab)

        self.setLayout(self._layout)

    def scriptModule(self, name):
        if name in self._pyModules:
            return self._pyModules[name]

    def module_count(self) -> int:
        return len(self._pyModules)

    def modules(self):
        return self._pyModules

    def newTab(self, index):
        if self._tab_widget.tabText(index) == "+":
            new_pyModule = UIEditorScript.ScriptEditor()
            self._tab_widget.insertTab(index, new_pyModule, f'PyModule_{index+1}')
            self._pyModules[f'PyModule_{index+1}'] = new_pyModule

    def newTabCode(self,index, name, code):
        if name not in self._pyModules:
            new_pyModule = UIEditorScript.ScriptEditor()
            new_pyModule.appendPlainText(code)
            self._tab_widget.insertTab(index, new_pyModule, name)
            self._pyModules[name] = new_pyModule

        else:
            self._pyModules[name].appendPlainText(code)

    def closeTab(self, index):
        widget = self._tab_widget.widget(index)
        text = self._tab_widget.tabText(index)
        self._tab_widget.removeTab(index)
        editor_class = self._pyModules.pop(text)
        del widget, editor_class

    def move_line_back(self, state):
        widget = self._tab_widget.widget(self._tab_widget.currentIndex())
        widget.reverse_TabHandling()

    def move_line_forward(self, state):
        widget = self._tab_widget.widget(self._tab_widget.currentIndex())
        widget.tab_effect()

    def comment_action(self, state):
        widget = self._tab_widget.widget(self._tab_widget.currentIndex())
        widget.commentHandling()

    def zoom_in_call(self, state):
        widget = self._tab_widget.widget(self._tab_widget.currentIndex())
        widget.zoom_in()

    def zoom_out_call(self, state):
        widget = self._tab_widget.widget(self._tab_widget.currentIndex())
        widget.zoom_out()


