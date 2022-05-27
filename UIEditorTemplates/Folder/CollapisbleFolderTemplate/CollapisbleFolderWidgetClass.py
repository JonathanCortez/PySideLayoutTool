from PySide2 import QtWidgets, QtCore
from operator import add, sub

class CollapsibleFolderWidgetV2(QtWidgets.QWidget):
    def __init__(self, title):
        super(CollapsibleFolderWidgetV2, self).__init__()
        self._check = False
        self._title = title
        self._parent = None
        self._extra_size = [0,0]
        self._speed = 300

        self._button = QtWidgets.QToolButton(text=title, checkable=True, checked=False)
        self._button.setProperty('class','collapsible_folder')

        self._button.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Fixed)
        self._button.setFixedHeight(25)
        self._button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self._button.setArrowType(QtCore.Qt.RightArrow)

        self._frame = QtWidgets.QGroupBox()
        self._frame.setProperty('class','tab_box')

        self._frame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self._frame.setMaximumHeight(0)
        self._frame.setMinimumHeight(0)
        self._frame_layout = None

        self._contentArea = QtWidgets.QScrollArea()
        self._contentArea.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self._contentArea.setMaximumHeight(0)
        self._contentArea.setMinimumHeight(0)

        self._ToggleAnimation = QtCore.QParallelAnimationGroup(self)
        self._ToggleAnimation.addAnimation(QtCore.QPropertyAnimation(self, b"minimumHeight"))
        self._ToggleAnimation.addAnimation(QtCore.QPropertyAnimation(self, b"maximumHeight"))
        self._ToggleAnimation.addAnimation(QtCore.QPropertyAnimation(self._contentArea, b"maximumHeight"))

        self._mainLayout = QtWidgets.QVBoxLayout()
        self._mainLayout.setSpacing(0)
        self._mainLayout.setContentsMargins(0 ,0 ,0 ,0)
        self._mainLayout.setAlignment(QtCore.Qt.AlignTop)
        self._mainLayout.addWidget(self._button)
        self._mainLayout.addWidget(self._frame)
        self._mainLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)

        self.setLayout(self._mainLayout)

        self._button.clicked.connect(self.buttonClicked)
        self._ToggleAnimation.finished.connect(self.animeFinished)

    def button_widget(self):
        return self._button

    def addParent(self, parent):
        self._parent = parent

    def setTitle(self, text_str: str):
        self._button.setText(text_str)

    def buttonClicked(self):
        checked = self._button.isChecked()
        self._check = checked
        if self._check:
            self._button.setArrowType(QtCore.Qt.DownArrow)
            self._ToggleAnimation.setDirection(QtCore.QAbstractAnimation.Forward)
            self._ToggleAnimation.start()
            self._frame.setMaximumHeight(self._frame_layout.sizeHint().height())
            self._frame.setMinimumHeight(self._frame_layout.sizeHint().height())

        else:
            self._button.setArrowType(QtCore.Qt.RightArrow)
            self._ToggleAnimation.setDirection(QtCore.QAbstractAnimation.Backward)
            self._ToggleAnimation.start()


    def animeFinished(self):
        if not self._check:
            self._frame.setMaximumHeight(0)
            self._frame.setMinimumHeight(0)

    def force_close(self):
        self._frame.setMaximumHeight(0)
        self._frame.setMinimumHeight(0)

    def init_open(self, arg: bool):
        if arg:
            self._frame.setMaximumHeight(self._frame_layout.sizeHint().height())
            self._frame.setMinimumHeight(self._frame_layout.sizeHint().height())
            self._button.setChecked(arg)
            self._button.setArrowType(QtCore.Qt.DownArrow)


    def setContentLayout(self, layout, open:bool = False, speed: int = 300):
        self._frame.setLayout(layout)
        self._frame_layout = layout
        self._speed = speed

        collapsedHeight = (self.sizeHint().height() - self._frame.maximumHeight())
        content_height = layout.sizeHint().height()

        for i in range(self._ToggleAnimation.animationCount()):
            animation = self._ToggleAnimation.animationAt(i)
            animation.setDuration(speed)
            animation.setStartValue(collapsedHeight)
            animation.setEndValue(collapsedHeight + content_height)

        contentAnimation = self._ToggleAnimation.animationAt(self._ToggleAnimation.animationCount() - 1)
        contentAnimation.setDuration(speed)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(content_height)
        self.init_open(open)


    def collapisble_layout(self):
        return self._frame.layout()

    def updateSize(self, width, height, add_size = True):
        self._extra_size[0] = width
        self._extra_size[1] = height
        content_height = add(self._frame_layout.sizeHint().height() ,self._extra_size[1]) #if add_size else sub(self._frame_layout.sizeHint().height() ,self._extra_size[1])

        if add_size:
            self._frame.setMaximumHeight(content_height)
            self._frame.setMinimumHeight(content_height)

            collapsedHeight = add((self.sizeHint().height() - self._frame.maximumHeight()),self._extra_size[1]) #if add_size else sub((self.sizeHint().height() - self._frame.maximumHeight()),self._extra_size[1])

            for i in range(self._ToggleAnimation.animationCount()):
                animation = self._ToggleAnimation.animationAt(i)
                animation.setDuration(self._speed)
                animation.setStartValue(collapsedHeight)
                animation.setEndValue(collapsedHeight + content_height)

            contentAnimation = self._ToggleAnimation.animationAt(self._ToggleAnimation.animationCount() - 1)
            contentAnimation.setDuration(self._speed)
            contentAnimation.setStartValue(0)
            contentAnimation.setEndValue(content_height)



class CollapsibleFolderWidget(QtWidgets.QWidget):

    def __init__(self, child_widget_layout):
        super(CollapsibleFolderWidget, self).__init__()

        self._check = False
        self._child_widget = child_widget_layout

        self._button = QtWidgets.QToolButton(text='None', checkable=True, checked=False)
        self._button.setProperty('class', 'collapsible_folder')

        self._button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self._button.setFixedHeight(25)
        self._button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self._button.setArrowType(QtCore.Qt.RightArrow)

        self._frame = QtWidgets.QGroupBox()
        self._frame.setProperty('class', 'tab_box')
        self._frame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self._frame.setVisible(False)

        self.update_layout(child_widget_layout)

        self._mainLayout = QtWidgets.QVBoxLayout()
        self._mainLayout.setSpacing(0)
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.setAlignment(QtCore.Qt.AlignTop)

        self._mainLayout.addWidget(self._button)
        self._mainLayout.addWidget(self._frame)
        self.setLayout(self._mainLayout)

        self._button.clicked.connect(self._button_clicked)

    def folder_title(self, text: str):
        self._button.setText(text)

    def open_folder(self, state: bool):
        self._button_clicked(state)
        self._button.setChecked(state)

    def collapisble_layout(self):
        return self._frame.layout()

    def update_layout(self, widget_layout):
        self._child_widget = widget_layout

        if isinstance(self._child_widget, QtWidgets.QWidget):
            frame_layout = QtWidgets.QVBoxLayout()
            frame_layout.setSpacing(0)
            frame_layout.setContentsMargins(0, 0, 0, 0)
            frame_layout.addWidget(self._child_widget)
            self._frame.setLayout(frame_layout)

        else:
            self._frame.setLayout(self._child_widget)


    def new_frame(self, new_widget):
        self._mainLayout.itemAt(1).widget().deleteLater()

        self._frame = QtWidgets.QGroupBox()
        self._frame.setProperty('class', 'tab_box')
        self._frame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self._frame.setVisible(False)
        self.update_layout(new_widget)

        self._mainLayout.addWidget(self._frame)


    def _button_clicked(self, state):
        self._check = state
        if self._check:
            self._button.setArrowType(QtCore.Qt.DownArrow)
            self._frame.setVisible(True)
        else:
            self._button.setArrowType(QtCore.Qt.RightArrow)
            self._frame.setVisible(False)