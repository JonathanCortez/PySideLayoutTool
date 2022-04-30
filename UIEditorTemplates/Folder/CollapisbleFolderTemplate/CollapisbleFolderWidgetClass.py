from PySide2 import QtWidgets, QtCore

class CollapsibleFolderWidget(QtWidgets.QWidget):
    def __init__(self, title):
        super(CollapsibleFolderWidget, self).__init__()
        self._check = False
        self._title = title
        self._parent = None
        self._extra_size = (0,0)

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
            self._frame.setMaximumHeight(self._frame_layout.sizeHint().height() + self._extra_size[1])
            self._frame.setMinimumHeight(self._frame_layout.sizeHint().height() + self._extra_size[1])


        else:
            self._button.setArrowType(QtCore.Qt.RightArrow)
            self._ToggleAnimation.setDirection(QtCore.QAbstractAnimation.Backward)
            self._ToggleAnimation.start()


    def animeFinished(self):
        if not self._check:
            self._frame.setMaximumHeight(0)
            self._frame.setMinimumHeight(0)

    
    def init_open(self, arg: bool):
        if arg:
            self._frame.setMaximumHeight(self._frame_layout.sizeHint().height() + self._extra_size[1])
            self._frame.setMinimumHeight(self._frame_layout.sizeHint().height() + self._extra_size[1])
            self._button.setChecked(arg)
            self._button.setArrowType(QtCore.Qt.DownArrow)


    def setContentLayout(self, layout, open:bool = False, speed: int = 300):
        self._frame.setLayout(layout)
        self._frame_layout = layout

        self.init_open(open)
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


    def collapisble_layout(self):
        return self._frame.layout()


    def updateSize(self, width, height):
        self._extra_size = (width, height)
        self._frame.setMaximumHeight(self._frame_layout.sizeHint().height() + 30)
        self._frame.setMinimumHeight(self._frame_layout.sizeHint().height() + 30)
        # TODO: Fix this to work properly before release.
        collapsedHeight = (self.sizeHint().height() - self._frame.maximumHeight())
        content_height = self._frame_layout.sizeHint().height() + 30

        for i in range(self._ToggleAnimation.animationCount()):
            animation = self._ToggleAnimation.animationAt(i)
            animation.setDuration(300)
            animation.setStartValue(collapsedHeight)
            animation.setEndValue(collapsedHeight + content_height)