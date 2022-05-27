from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import QObject, Signal
from PySideLayoutTool.UIEditorTemplates.Common.SeparatorTemplate import SeparatorWidgetClass

from math import degrees, radians, sqrt, atan2, sin, cos, pi, floor

class ColorButtonWidget(QtWidgets.QPushButton):

    def __init__(self, parent, bAlpha=False):
        super(ColorButtonWidget, self).__init__(parent)
        self.setMinimumWidth(40)
        self.setMaximumWidth(40)
        self._color_editor = colorPicker(bAlpha, parent=self)
        self.brushColor = QtGui.QBrush(QtGui.QColor(255, 255, 255, 255))
        self._color = None

        self.pressed.connect(self.openColorEditor)

    def openColorEditor(self):
        self._color_editor.show()

    def colorPickerWidget(self):
        return self._color_editor

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setBrush(self.brushColor)
        painter.drawRoundedRect(5,1,30,15,2,2)

    def updateButtonColor(self,color):
        self._color = color
        self.brushColor = QtGui.QBrush(color)
        self.update()

#TODO: ADD checker pattern for color with alpha on button rect.

class ColorObject(QObject):
    colorSignal = Signal(QtGui.QColor)


class colorPicker(QtWidgets.QDialog):
    "custom colorDialog from Orthallelous"
    # currentColorChanged = ColorObject()
    # colorSelected = ColorObject()

    def __init__(self,bAlpha, initial=None, parent=None):
        super(colorPicker, self).__init__(parent)
        self.currentColorChanged = ColorObject()
        self.colorSelected = ColorObject()
        self._use_Aplha = bAlpha
        self.setup()
        self.setColor(initial)


    def mapRange_Clamp(self,value, inRangeA, inRangeB, outRangeA, outRangeB):
        if outRangeA == outRangeB: return outRangeA
        if inRangeA == inRangeB: Exception("inRangeA == inRangeB which will produce one to many mapping")
        inPercentage = (value - inRangeA) / (inRangeB - inRangeA)
        if inPercentage < 0.0: return outRangeA
        if inPercentage > 1.0: return outRangeB;
        return outRangeA + inPercentage * (outRangeB - outRangeA)


    def currentColor(self):
        return self._color

    def setColor(self, qcolor=None):
        if qcolor is None:
            self._color = QtGui.QColor('#ffffff')
        else:
            self._color = QtGui.QColor(qcolor)
        self._colorEdited()

    @staticmethod
    def getColor(initial=None, parent=None, title=None):
        dialog = colorPicker(initial, parent)
        if title: dialog.setWindowTitle(title)
        result = dialog.exec_()
        color = dialog._color
        return color

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def closeValid(self):
        "emits colorSelected signal with valid color on OK"
        self.currentColorChanged.colorSignal.emit(self._color)
        self.colorSelected.colorSignal.emit(self._color)
        self.close()

    def closeInvalid(self):
        "emits colorSelected signal with invalid color on Cancel"
        self._color = QtGui.QColor()
        self.colorSelected.colorSignal.emit(QtGui.QColor())
        self.close()

    def setOption(self, option, Bool=True):
        if option == QtWidgets.QColorDialog.NoButtons:
            if not Bool:
                self.dialogButtons.blockSignals(False)
                self.dialogButtons.setEnabled(True)
                self.dialogButtons.show()
            else:
                self.dialogButtons.blockSignals(True)
                self.dialogButtons.setEnabled(False)
                self.dialogButtons.hide()
        self.setFixedSize(self.sizeHint())


    def _colorEdited(self):
        "internal color editing"
        sender, color = self.sender(), self._color
        for i in self.inputs: i.blockSignals(True)
        for i in self.colorRects.RGBInputs() + self.colorRects.HSVInputs(): i.blockSignals(True)

        # get values
        if sender in self.colorRects.RGBInputs():
            color.setRgbF(*[i.value() for i in self.colorRects.RGBInputs()])
        elif sender in self.colorRects.HSVInputs():
            hsvValue = [self.colorRects.HSVInputs()[0].value()]
            for i in self.colorRects.HSVInputs()[1:]:
                hsvValue.append(int(self.mapRange_Clamp(i.value(),0,1,0,255)))
            color.setHsv(*hsvValue)
        # elif sender in self.colorRects.TMIInputs():
        #     tempValue = self.colorRects.TMIInputs()[0].value()
        #     redGain = 1 - tempValue/2
        #     blueGain = 1 + tempValue/2
        #     color.setRedF(redGain)
        #     color.setBlueF(blueGain)
        elif sender is self.htmlInput:  # HTML
            color.setNamedColor('#' + str(self.htmlInput.text()).lower())
        elif sender is self.colorWheel:  # WHEEL
            color = self._color = self.colorWheel.getColor()
        elif sender is self.colorNamesCB:  # NAMED
            dat = self.colorNamesCB.itemData(self.colorNamesCB.currentIndex())
            color = self._color = QtGui.QColor(str(dat))  # PySide
            self.colorNamesCB.setToolTip(self.colorNamesCB.currentText())
        elif isinstance(sender,QtWidgets.QPushButton):
            value = sender.palette().window().color().getRgbF()
            color.setRgbF(*value)
        elif isinstance(sender, QtWidgets.QDoubleSpinBox):
            rgba = sender.parent().parent().eval()
            if len(rgba) == 3:
                color.setRgbF(float(rgba[0]), float(rgba[1]), float(rgba[2]))
            else:
                color.setRgbF(float(rgba[0]), float(rgba[1]), float(rgba[2]))
                color.setAlphaF(float(rgba[3]))

        else:
            pass

        if self._use_Aplha:
            color.setAlphaF(self.colorRects.AlphaInput().value())


        # set Values
        self.parent().updateButtonColor(color)
        self.parent().parent().setValue(color.getRgbF())
        self.colorRects.setColors(color)
        self.htmlInput.setText(color.name()[1:])
        self.colorWheel.setColor(color)
        # idx = self.colorNamesCB.findData(color.name())
        # self.colorNamesCB.setCurrentIndex(idx)  # will be blank if not in list

        pal = self.colorDisplay.palette()
        pal.setColor(self.colorDisplay.backgroundRole(), color)
        self.colorDisplay.setPalette(pal)
        self.colorDisplay.setStyleSheet('background:' + color.name())

        for i in self.inputs: i.blockSignals(False)
        for i in self.colorRects.RGBInputs() + self.colorRects.HSVInputs(): i.blockSignals(False)
        self.currentColorChanged.colorSignal.emit(color)

    def pickColor(self):
        "pick a color on the screen, part 1"
        desktop = QtWidgets.QApplication.desktop().winId()  # screenshot the desktop
        self._img = QtGui.QPixmap.grabWindow(desktop, 0, 0, -1, -1)

        self._view = QtWidgets.QGraphicsView(self)
        scene = QtWidgets.QGraphicsScene(self)  # display screenshot at full size

        self._view.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self._view.setWindowFlags(QtCore.Qt.WindowType_Mask)
        self._view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scene.addPixmap(self._img)
        self._view.setScene(scene)

        self._appview = QtWidgets.QApplication
        self._appview.setOverrideCursor(QtCore.Qt.PointingHandCursor)

        self._view.showFullScreen()
        self._view.mousePressEvent = self._pickedColor

    def _pickedColor(self, event):
        "pick a color on the screen, part 2"
        color = QtGui.QColor(self._img.toImage().pixel(event.globalPos()))

        self._view.hide()
        self._appview.restoreOverrideCursor()
        self._color = color
        self._colorEdited()
        self._appview = self._view = self._img = None  # delete screenshot

    def showColors(self):
        "show location of colors on color wheel"
        if self.showButton.isChecked():
            self.colorWheel.showNamedColors(True)
        else:
            self.colorWheel.showNamedColors(False)

    def getNamedColors(self):
        "returns a list [(name, #html)] from the named colors combobox"
        lst = []
        for i in range(self.colorNamesCB.count()):
            name = str(self.colorNamesCB.itemText(i))
            try:  # PyQt
                html = str(self.colorNamesCB.itemData(i).toString())
            except AttributeError:  # PySide
                html = str(self.colorNamesCB.itemData(i))
            lst.append((name, html))
        return lst

    def addNamedColors(self, lst):
        "add a list [('name', '#html'), ] of named colors (repeats removed)"
        col = self.getNamedColors() + lst
        lst = [(i[0], QtGui.QColor(i[1])) for i in col]
        sen = set()
        add = sen.add  # http://stackoverflow.com/a/480227
        uni = [x for x in lst if not (x[1].name() in sen or add(x[1].name()))]

        self.colorNamesCB.clear()
        for i, j in sorted(uni, key=lambda q: q[1].getHsv()):
            icon = QtGui.QPixmap(16, 16)
            icon.fill(j)
            self.colorNamesCB.addItem(QtGui.QIcon(icon), i, j.name())
        self.colorWheel.setNamedColors([(i, j.name()) for i, j in uni])
        self.cNameLabel.setToolTip('Named colors\n{:,} colors'.format(len(uni)))

    def setup(self):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        fixed = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                      QtWidgets.QSizePolicy.Fixed)
        rightCenter = (QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)


        #Dialog Splitter
        self.splitter = QtWidgets.QSplitter()
        self.splitter.setChildrenCollapsible(False)

        #Right Side Setup
        self.rightLayout = QtWidgets.QVBoxLayout()
        self.rightLayout.setSpacing(5)
        self.rightLayout.setContentsMargins(0,2,0,2)

        self.rightWidget = QtWidgets.QWidget()
        self.rightWidget.setLayout(self.rightLayout)

        #Left Side Setup
        self.leftLayout = QtWidgets.QVBoxLayout()
        self.leftLayout.setSpacing(5)
        self.leftLayout.setContentsMargins(5, 2, 5, 2)

        self.leftWidget = QtWidgets.QWidget()

        #Color Rects
        self.colorRects = ColorEditorRightLayout(self,self._use_Aplha)

        # HTML
        self.htmlInput = QtWidgets.QLineEdit()
        self.htmlInput.setFixedSize(35 + 22, 22)  # spans 2 cols
        self.htmlInput.setPlaceholderText('html')
        self.htmlInput.setAlignment(QtCore.Qt.AlignCenter)
        regex = QtCore.QRegExp('[0-9A-Fa-f]{1,6}')
        valid = QtGui.QRegExpValidator(regex)
        self.htmlInput.setValidator(valid)

        self.htmlLabel = QtWidgets.QLabel('&#')
        self.htmlLabel.setToolTip('Web color')
        self.htmlLabel.setBuddy(self.htmlInput)

        self.htmlLabel.setFixedSize(22, 22)
        self.htmlLabel.setAlignment(rightCenter)

        self.htmlInput.editingFinished.connect(self._colorEdited)

        # picker button
        self.pickButton = QtWidgets.QPushButton('&Pick')
        self.pickButton.setToolTip('Pick a color from the screen')
        self.pickButton.setFixedSize(35, 22)
        self.pickButton.clicked.connect(self.pickColor)

        # color display
        self.colorDisplay = QtWidgets.QFrame()
        self.colorDisplay.setFixedSize(180, 70)  # spans 4 rows
        self.colorDisplay.setFrameShape(QtWidgets.QFrame.Panel)
        self.colorDisplay.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.colorDisplay.setAutoFillBackground(True)

        # show button / random button
        # self.showButton = QtWidgets.QPushButton('Sho&w')
        # self.showButton.setToolTip('Show named colors on color wheel')
        # self.showButton.setFixedSize(35, 22)
        # self.showButton.setCheckable(True)
        # self.showButton.clicked.connect(self.showColors)

        # color wheel
        self.colorWheel = ColorWheel()
        self.colorWheel.setFixedSize(256, 256)  # 265, 265)
        self.colorWheel.currentColorChanged.colorSignal.connect(self.setColor)

        # named colors combo box
        self.colorNamesCB = QtWidgets.QComboBox()
        self.colorNamesCB.setFixedSize(70 + 66 + 4, 22)  # spans 5 cols
        # self.colorNamesCB.addItem('- Color Names -')

        self.cNameLabel = QtWidgets.QLabel('&Named:')
        self.cNameLabel.setBuddy(self.colorNamesCB)
        self.cNameLabel.setAlignment(rightCenter)
        # self.cNameLabel.setFrameShape(QtGui.QFrame.Box)
        self.cNameLabel.setFixedSize(55, 22)

        lst = [i for i in QtGui.QColor.colorNames() if str(i) != 'transparent']
        lst = [(i, QtGui.QColor(i)) for i in lst]
        lst.append(('Cosmic latte', '#fff8e7'))
        lst.append(('rebeccapurple', '#663399'))
        self.addNamedColors(lst)
        self.colorNamesCB.currentIndexChanged.connect(self._colorEdited)

        self.inputs = [self.htmlInput, self.colorWheel, self.colorNamesCB]

        # ok/cancel buttons
        self.dialogButtons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok
                                                    | QtWidgets.QDialogButtonBox.Cancel)
        self.dialogButtons.accepted.connect(self.closeValid)
        self.dialogButtons.rejected.connect(self.closeInvalid)
        self.dialogButtons.setCenterButtons(True)
        # pass QtGui.QColorDialog.NoButtons, False to setOption to remove

        #Layout Setup
        self.leftLayout.addWidget(self.colorWheel)
        self.leftLayout.addWidget(SeparatorWidgetClass.SeparatorHWidget())

        color_frame = QtWidgets.QGroupBox('Previous/Current Color')
        color_frame.setFixedSize(260, 100)

        color_frame_layout = QtWidgets.QHBoxLayout()
        color_frame_layout.setSpacing(0)
        color_frame_layout.setContentsMargins(0,10,0,10)

        color_frame_layout.addWidget(self.colorDisplay)

        color_frame_layout_buttons = QtWidgets.QVBoxLayout()
        color_frame_layout_buttons.setSpacing(5)
        color_frame_layout_buttons.setContentsMargins(0, 0, 0, 0)
        color_frame_layout_buttons.setAlignment(QtCore.Qt.AlignTop)

        color_frame_layout_buttons.addWidget(self.pickButton)
        color_frame_layout.addLayout(color_frame_layout_buttons)
        color_frame.setLayout(color_frame_layout)

        self.leftLayout.addWidget(color_frame)
        self.leftLayout.addWidget(SeparatorWidgetClass.SeparatorHWidget())

        html_frame = QtWidgets.QGroupBox('HTML Format')
        html_frame.setFixedSize(260, 50)

        html_frame_layout = QtWidgets.QVBoxLayout()
        html_frame_layout.setSpacing(0)
        html_frame_layout.setContentsMargins(5, 10, 5, 10)
        html_frame_layout.setAlignment(QtCore.Qt.AlignTop)

        html_layout = QtWidgets.QHBoxLayout()
        html_layout.setSpacing(5)
        html_layout.setAlignment(QtCore.Qt.AlignLeft)

        html_layout.addWidget(self.htmlLabel)
        html_layout.addWidget(self.htmlInput)

        html_frame_layout.addLayout(html_layout)
        html_frame.setLayout(html_frame_layout)

        self.leftLayout.addWidget(html_frame)

        self.leftWidget.setLayout(self.leftLayout)
        self.rightLayout.addWidget(self.colorRects)

        self.baselayout = QtWidgets.QVBoxLayout()
        self.baselayout.setSpacing(0)
        self.baselayout.setContentsMargins(0,0,0,0)
        self.baselayout.setAlignment(QtCore.Qt.AlignTop)

        self.splitter.addWidget(self.leftWidget)
        self.splitter.addWidget(self.rightWidget)

        self.baselayout.addWidget(self.splitter)

        self.setWindowTitle('Color Editor')
        ico = self.style().standardIcon(QtWidgets.QStyle.SP_DialogResetButton)
        self.setWindowIcon(ico)
        self.setLayout(self.baselayout)
        self.setFixedSize(self.sizeHint())


class ColorRect(QtWidgets.QWidget):

    def __init__(self):
        super(ColorRect, self).__init__()
        self.setMaximumHeight(32)
        self.setMinimumHeight(32)
        self.setMinimumWidth(265)
        self.setMaximumWidth(265)
        self.start = 4

        self.frame_color = None
        self.linearGrad = QtGui.QLinearGradient(5, 5, 255, 25)
        self.linearBrush = QtGui.QBrush(self.linearGrad)

    def paintEvent(self, event) -> None:
        painter = QtGui.QPainter(self)
        painter.setBrush(self.linearBrush)
        painter.drawRect(self.start, 6, 255, 20)

    def setColor(self, colors):
        self.frame_color = colors
        for i, c in enumerate(self.frame_color[::-1]):
            self.linearGrad.setColorAt(i / (len(colors) - 1), c)

        self.linearBrush = QtGui.QBrush(self.linearGrad)
        self.update()


class AlphaRect(QtWidgets.QWidget):

    def __init__(self, parent):
        super(AlphaRect, self).__init__(parent)
        self.setMaximumHeight(30)
        self.setMinimumHeight(30)
        self.setMinimumWidth(256)
        self.setMaximumWidth(256)
        self.linearBrush = QtGui.QBrush()
        self.checkerImage = QtGui.QPixmap('/PySideLayoutTool/Resources/Icons/checkerPattern.png')
        self.linearBrush.setTexture(self.checkerImage)

    def paintEvent(self, event) -> None:
        painter = QtGui.QPainter(self)
        painter.setBrush(self.linearBrush)
        painter.drawRect(4, 5, 255, 20)


class ColorRectSlider(QtWidgets.QSlider):

    def __init__(self,parent, minValue=0, maxValue=1, bfloat=True):
        super(ColorRectSlider, self).__init__(parent)
        self.min = minValue * 1000000.0 if bfloat else minValue
        self.max = maxValue * 1000000.0 if bfloat else maxValue
        self.bFloat = bfloat

        self.setOrientation(QtCore.Qt.Horizontal)
        self.setStyleSheet('QSlider::groove:horizontal { height: 0px; }'
                            'QSlider::handle:horizontal { margin-top: -12px; margin-bottom: -12px; width: 6px; }'
                            'QSlider { background-color: none; }')

        self.setRange(int(self.min), int(self.max))

    def useFloat(self):
        return self.bFloat

    def sizeHint(self):
        return QtCore.QSize(265, 35)


class ColorRectLayout(QtWidgets.QWidget):

    def __init__(self,dialog, label: str, tooltip: str,bAlpha=False, minRange=0, maxRange=1,bFloat=True):
        super(ColorRectLayout, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.setAlignment(QtCore.Qt.AlignTop)

        self._hor_layout = QtWidgets.QHBoxLayout()
        self._hor_layout.setSpacing(5)
        self._hor_layout.setContentsMargins(0,0,0,0)
        self._hor_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.dialog_obj = dialog
        self.name = label
        self.minValue = minRange
        self.maxValue = maxRange

        self.input_widget = QtWidgets.QDoubleSpinBox(self) if bFloat else QtWidgets.QSpinBox(self)
        self.input_widget.setRange(-15, 15) if bFloat else self.input_widget.setRange(self.minValue, self.maxValue)
        self.input_widget.setSingleStep(0.1) if bFloat else self.input_widget.setSingleStep(1)
        self.input_widget.setFixedSize(40,20)
        self.input_widget.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

        self.label_widget = QtWidgets.QLabel(label)
        self.label_widget.setToolTip(tooltip)
        self.label_widget.setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")

        self.label_widget.setBuddy(self.input_widget)

        self.colorRectDisplay = ColorRect()
        if bAlpha:
            AlphaRect(self.colorRectDisplay)
        self.colorSlider = ColorRectSlider(self.colorRectDisplay, minRange, maxRange, bFloat)


        self._hor_layout.addWidget(self.label_widget)
        self._hor_layout.addWidget(self.input_widget)
        self._hor_layout.addSpacing(5)
        self._hor_layout.addWidget(self.colorRectDisplay)

        self._layout.addLayout(self._hor_layout)
        self.setLayout(self._layout)

        self.input_widget.valueChanged.connect(dialog._colorEdited)
        self.colorSlider.valueChanged.connect(self.updateColors)


    def input(self):
        return self.input_widget

    def updateColors(self,value):
        sender = self.sender()
        value = value

        if sender.useFloat():
            value = float(value / 1000000.0)
        self.input_widget.setValue(value)


    def updateValues(self, value):
        self.input_widget.blockSignals(True)
        self.input_widget.setValue(value)
        self.colorSlider.setValue(value * 1000000.0 if self.colorSlider.useFloat() else value)
        self.input_widget.blockSignals(False)

    def updateRectColor(self,color):
        self.colorRectDisplay.setColor(color)




class ColorEditorRightLayout(QtWidgets.QWidget):

    def __init__(self, parent, useAlpha):
        super(ColorEditorRightLayout, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(5, 10, 5, 10)
        self._layout.setAlignment(QtCore.Qt.AlignTop)
        self.parent = parent
        self._color = None
        self._useAlpha = useAlpha

        self._colorButtons = ColorListButtons(parent)

        #RGBA Setup
        self.redWidget = ColorRectLayout(parent,'&R:','Red')
        self.greenWidget = ColorRectLayout(parent,'&G:','Green')
        self.blueWidget = ColorRectLayout(parent,'&B:','Blue')
        self.alphaWidget = ColorRectLayout(parent,'&A:','Alpha',self._useAlpha) if useAlpha else None
        self.rgbInputs = [self.redWidget.input(), self.greenWidget.input(), self.blueWidget.input()]

        #HSV Setup
        hueColors = [QtCore.Qt.red, QtCore.Qt.magenta, QtCore.Qt.blue,
                     QtCore.Qt.cyan, QtCore.Qt.green,
                     QtCore.Qt.yellow, QtCore.Qt.red]

        self.hueWidget = ColorRectLayout(parent,'&H:','Hue',maxRange=360,bFloat=False)
        self.hueWidget.updateRectColor(hueColors)
        self.satWidget = ColorRectLayout(parent,'&S:','Saturation')
        self.valWidget = ColorRectLayout(parent,'&V:','Value')
        self.hsvInputs = [self.hueWidget.input(), self.satWidget.input(), self.valWidget.input()]

        #TMI Setup
        # self.TempWidget= ColorRectLayout(parent,'&T:','Temperature',minRange=-1,maxRange=1)
        # self.magentaWidget = ColorRectLayout(parent,'&M:','Magenta',minRange=-1,maxRange=1)
        # self.intensityWidget = ColorRectLayout(parent,'&I:','Intensity')
        # self.tmiInputs = [self.TempWidget.input(), self.magentaWidget.input(), self.intensityWidget.input()]

        self._layout.addWidget(self._colorButtons)
        self._layout.addWidget(SeparatorWidgetClass.SeparatorHWidget())

        self._layout.addWidget(self.redWidget)
        self._layout.addWidget(self.greenWidget)
        self._layout.addWidget(self.blueWidget)
        if self._useAlpha:
            self._layout.addWidget(self.alphaWidget)

        self._layout.addWidget(SeparatorWidgetClass.SeparatorHWidget())

        self._layout.addWidget(self.hueWidget)
        self._layout.addWidget(self.satWidget)
        self._layout.addWidget(self.valWidget)
        self._layout.addWidget(SeparatorWidgetClass.SeparatorHWidget())

        # self._layout.addWidget(self.TempWidget)
        # self._layout.addWidget(self.magentaWidget)
        # self._layout.addWidget(self.intensityWidget)

        self.setLayout(self._layout)

    def RGBInputs(self):
        return self.rgbInputs

    def HSVInputs(self):
        return self.hsvInputs

    def TMIInputs(self):
        return self.tmiInputs

    def AlphaInput(self):
        return self.alphaWidget.input()

    def setColors(self, color_obj):
        self._color = color_obj
        color = color_obj.getRgb()

        #RGB
        redRect = [QtGui.QColor(255, color[1], color[2], 255),
                   QtGui.QColor(0, color[1], color[2], 255)]
        self.redWidget.updateRectColor(redRect)
        self.redWidget.updateValues(color_obj.getRgbF()[0])

        greenRect = [QtGui.QColor(color[0], 255, color[2], 255),
                     QtGui.QColor(color[0], 0, color[2], 255)]
        self.greenWidget.updateRectColor(greenRect)
        self.greenWidget.updateValues(color_obj.getRgbF()[1])

        blueRect = [QtGui.QColor(color[0], color[1], 255, 255),
                    QtGui.QColor(color[0], color[1], 0, 255)]
        self.blueWidget.updateRectColor(blueRect)
        self.blueWidget.updateValues(color_obj.getRgbF()[2])

        if self._useAlpha:
            alphaRect = [QtGui.QColor(color[0], color[1], color[2], 255),
                         QtGui.QColor(color[0], color[1], color[2], 0)]
            self.alphaWidget.updateRectColor(alphaRect)
            self.alphaWidget.updateValues(color_obj.alphaF())

        #HSV
        self.hueWidget.updateValues(color_obj.hsvHue())

        hueColor = self.parent.mapRange_Clamp(color_obj.getHsv()[0], 0, 360, 0, 1)
        newcolor = QtGui.QColor()
        newcolor.setHsvF(hueColor, 1, 1)
        satRect = [newcolor, QtCore.Qt.white]
        self.satWidget.updateRectColor(satRect)
        self.satWidget.updateValues(color_obj.getHsvF()[1])

        valRect = [QtGui.QColor(color[0], color[1], color[2], 255),
                   QtCore.Qt.black]
        self.valWidget.updateRectColor(valRect)
        self.valWidget.updateValues(color_obj.getHsvF()[2])

        # TMI
        # colorF = color_obj.getRgbF()
        # redGain = colorF[0]
        # blueGain = colorF[2]
        # redhalf = self.parent.mapRange_Clamp(color[0],0,255,127,255)
        # bluehalf = self.parent.mapRange_Clamp(color[2],0,255,127,255)
        # t = self.parent.mapRange_Clamp(self.TempWidget.input().value(),-1,1,-225,225)
        # print(int(255 + int(t)/2))
        # tempRect = [QtGui.QColor(0, color[1], 255, color[3]),
        #             QtGui.QColor(color[0]/2, color[1], color[2]/2, color[3]).lighter(140),
        #             QtGui.QColor(255, color[1], 0, color[3])]
        # self.TempWidget.updateRectColor(tempRect)
        # self.TempWidget.updateValues(blueGain - redGain)


class ColorListButtons(QtWidgets.QWidget):

    def __init__(self,parent):
        super(ColorListButtons, self).__init__()
        self._base_layout = QtWidgets.QVBoxLayout()
        self._base_layout.setSpacing(0)
        self._base_layout.setContentsMargins(0, 0, 0, 0)
        self.parent = parent

        self._first_row = [[1,0,0],[1,0.5,0], [1,1,0], [0.5,1,0], [0,1,0],
                           [0,1,0.5], [0,1,1], [0,0.5,1], [0,0,1],
                           [0.5,0,1], [1,0,1], [1,0,0.5]]

        self._second_row = [ [i/2 for i in x] for x in self._first_row]

        self._third_row = [[0.3,0.075,0.075], [0.3, 0.1875, 0.075],[0.3, 0.3, 0.075],
                           [0.1875, 0.3, 0.075], [0.075, 0.3, 0.075], [0.075, 0.3, 0.1875],
                           [0.075,0.3,0.3], [0.075,0.1875,0.3], [0.075, 0.075, 0.3],
                           [0.1875, 0.075, 0.3], [0.3,0.075, 0.3], [0.3, 0.075,0.1875]]

        self._fourth_row = [[0,0,0], [0.00625, 0.00625, 0.00625], [0.0125, 0.0125, 0.0125],
                            [0.025,0.025,0.025], [0.05,0.05,0.05], [0.1,0.1,0.1],[0.2,0.2,0.2],
                            [0.333,0.333,0.333],[0.5,0.5,0.5], [0.6667,0.6667,0.6667], [0.75,0.75,0.75], [1,1,1]]

        self._color_list = [self._first_row, self._second_row, self._third_row, self._fourth_row]

        self._frame = QtWidgets.QGroupBox('Color List')

        self._frame_layout = QtWidgets.QVBoxLayout()
        self._frame_layout.setSpacing(2)
        self._frame_layout.setContentsMargins(5, 10, 5, 10)
        self._frame_layout.setAlignment(QtCore.Qt.AlignTop)

        self._frame.setLayout(self._frame_layout)
        self._base_layout.addWidget(self._frame)

        for i in range(0,4):
            self.addhorizational_Buttons(self._color_list[i])

        self.setLayout(self._base_layout)

    def addhorizational_Buttons(self, color_list):
        hor_layout = QtWidgets.QHBoxLayout()
        hor_layout.setSpacing(2)
        hor_layout.setContentsMargins(0, 0, 0, 0)
        hor_layout.setAlignment(QtCore.Qt.AlignLeft)

        for i in range(0,12):
            current_color = color_list[i]
            r = floor(current_color[0] * 255)
            g = floor(current_color[1] * 255)
            b = floor(current_color[2] * 255)

            button = QtWidgets.QPushButton(self)
            button.setMinimumHeight(30)
            button.setMaximumHeight(30)
            button.setMaximumWidth(25)
            button.setStyleSheet("QPushButton { background-color:" + f"rgb({r},{g},{b})"+";}"
                                 "QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")
            button.setToolTip(f'({current_color[0]}, {current_color[1]}, {current_color[2]}) \n LMB to select')
            button.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Fixed)
            hor_layout.addWidget(button)
            button.pressed.connect(self.parent._colorEdited)

        self._frame_layout.addLayout(hor_layout)


class ColorWheel(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(ColorWheel, self).__init__(parent)
        self.setFixedSize(256, 256)
        self.currentColorChanged = ColorObject()

        # start, end angles for value arc
        self.s_ang, self.e_ang = 135, 225

        # offset angle and direction for color wheel
        self.o_ang, self.rot_d = 45, -1  # 1 for clock-wise, -1 for widdershins

        # other initializations
        self.pos = QtCore.QPointF(-100, -100)
        self.vIdCen = QtCore.QPointF(-100, -100)
        self.vIdAng = radians(self.s_ang)
        self.chPt = self.pos
        self.hue = self.sat = self.value = 255
        self.vIdBox = None
        self.vIdAng = None

        self.setup()
        self.pos = self.cWhBox.center()

        self._namedColorList = []
        self._namedColorPts = []
        self._showNames = False

        self.setMouseTracking(True)
        self.installEventFilter(self)

    def resizeEvent(self, event):
        self.setup()  # re-construct the sizes
        self.setNamedColors(self._namedColorList)

    def getColor(self):
        col = QtGui.QColor()
        col.setHsv(self.hue, self.sat, self.value)
        return col

    def setNamedColors(self, colorList):
        "sets list [(name, #html)] of named colors"
        self._namedColorList = colorList
        lst = []
        r2 = (self.vAoBox.width() + self.vAiBox.width()) / 4.0
        for i in self._namedColorList:
            h, s, v, a = QtGui.QColor(i[1]).getHsv()

            t = radians(h + self.o_ang * -self.rot_d) * -self.rot_d
            r = s / 255.0 * self.cW_rad
            x, y = r * cos(t) + self.cen.x(), r * -sin(t) + self.cen.y()
            lst.append(QtCore.QPointF(x, y))

            # t2 = ((v / 255.0) * self.ang_w + radians(self.e_ang) + 2 * pi) % (2 * pi)
            # x, y = r2 * cos(t2) + self.cen.x(), r2 * -sin(t2) + self.cen.y()
            # lst.append(QtCore.QPointF(x, y))
        self._namedColorPts = lst

    def showNamedColors(self, flag=False):
        "show/hide location of named colors on color wheel"
        self._showNames = flag
        self.update()

    def setColor(self, color):  # saturation -> radius
        h, s, v, a = color.getHsv()  # hue -> angle
        self.hue, self.sat, self.value = h, s, v  # value -> side bar thingy

        t = radians(h + self.o_ang * -self.rot_d) * -self.rot_d
        r = s / 255.0 * self.cW_rad
        x, y = r * cos(t) + self.cen.x(), r * -sin(t) + self.cen.y()
        self.chPt = QtCore.QPointF(x, y)  # hue, saturation

        self.vIdAng = t2 = (v / 255.0) * self.ang_w + radians(self.e_ang)
        self.vIdAng = t2 = t2 if t2 > 0 else t2 + 2 * pi
        r2 = self.vAoBox.width() / 2.0

        x, y = r2 * cos(t2) + self.cen.x(), r2 * -sin(t2) + self.cen.y()
        self.vIdCen, self.vIdAng = QtCore.QPointF(x, y), t2  # value
        self.vIdBox.moveCenter(self.vIdCen)
        self.update()

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.MouseButtonPress or
                (event.type() == QtCore.QEvent.MouseMove and
                 event.buttons() == QtCore.Qt.LeftButton)):
            self.pos = pos = event.pos()

            t = atan2(self.cen.y() - pos.y(), pos.x() - self.cen.x())
            if self.colWhlPath.contains(pos):  # in the color wheel
                self.chPt = pos

                # hue -> mouse angle (same as t here)
                h = (int(degrees(t)) - self.o_ang) * -self.rot_d
                self.hue = (h if h > 0 else h + 360) % 360

                # saturation -> mouse radius (clipped to wheel radius)
                m_rad = sqrt((self.pos.x() - self.cen.x()) ** 2 + (self.pos.y() - self.cen.y()) ** 2)
                self.sat = int(255 * min(m_rad / self.cW_rad, 1))

            if self.vArcPath.contains(pos):  # in the value selection arc
                self.vIdAng = t if t > 0 else t + 2 * pi
                r2 = self.vAoBox.width() / 2.0

                x, y = r2 * cos(t) + self.cen.x(), r2 * -sin(t) + self.cen.y()
                self.vIdCen = QtCore.QPointF(x, y)
                self.vIdBox.moveCenter(self.vIdCen)
                self.value = int(255 * (t - radians(self.e_ang)) / self.ang_w) % 256

            self.update()
            col = QtGui.QColor()
            col.setHsv(self.hue, self.sat, self.value)
            self.currentColorChanged.colorSignal.emit(col)

        return QtWidgets.QWidget.eventFilter(self, source, event)


    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.Antialiasing)

        # painter.setBrush(QtGui.QBrush(QtCore.Qt.black, QtCore.Qt.NoBrush))
        # painter.drawRect(self.winBox)  # border

        # value selector indicator
        painter.setBrush(QtGui.QBrush(QtCore.Qt.black, QtCore.Qt.SolidPattern))
        painter.drawPie(self.vIdBox, int(16 * (degrees(self.vIdAng) - 22.5)), 720)

        # value selector arc
        painter.setClipPath(self.vArcPath)
        painter.setPen(QtCore.Qt.NoPen)
        arc = QtGui.QConicalGradient(self.cen, self.e_ang)
        color = QtGui.QColor()
        color.setHsv(self.hue, self.sat, 255)
        arc.setColorAt(1 - (self.e_ang - self.s_ang) / 360.0, color)
        arc.setColorAt(1, QtCore.Qt.black)
        arc.setColorAt(0, QtCore.Qt.black)
        painter.setBrush(arc)
        painter.drawPath(self.vArcPath)
        painter.setClipPath(self.vArcPath, QtCore.Qt.NoClip)

        # color wheel
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self.cWhlBrush1)
        painter.drawEllipse(self.cWhBox)
        painter.setBrush(self.cWhlBrush2)
        painter.drawEllipse(self.cWhBox)

        # crosshairs
        painter.setClipPath(self.colWhlPath)
        painter.setBrush(QtGui.QBrush(QtCore.Qt.black, QtCore.Qt.SolidPattern))
        chVert = QtCore.QRectF(0, 0, 2, 20)
        chHort = QtCore.QRectF(0, 0, 20, 2)
        chVert.moveCenter(self.chPt)
        chHort.moveCenter(self.chPt)
        painter.drawRect(chVert)
        painter.drawRect(chHort)

        # named color locations
        if self._showNames:
            painter.setClipPath(self.vArcPath, QtCore.Qt.NoClip)
            painter.setPen(QtCore.Qt.SolidLine)
            painter.drawPoints(self._namedColorPts)  # PySide

    def setup(self):
        "sets bounds on value arc and color wheel"
        # bounding boxes
        self.winBox = QtCore.QRectF(self.rect())
        self.vIdBox = QtCore.QRectF()  # value indicator box
        self.vAoBox = QtCore.QRectF()  # value arc outer
        self.vAiBox = QtCore.QRectF()  # value arc inner
        self.cWhBox = QtCore.QRectF()  # color wheel

        self.vIdBox.setSize(QtCore.QSizeF(15, 15))
        self.vAoBox.setSize(self.winBox.size() - self.vIdBox.size() / 2.0)
        self.vAiBox.setSize(self.vAoBox.size() - QtCore.QSizeF(20, 20))
        self.cWhBox.setSize(self.vAiBox.size() - QtCore.QSizeF(20, 20))

        # center - shifted to the right slightly
        x = self.winBox.width() - (self.vIdBox.width() + self.vAiBox.width()) / 2.0
        self.cen = QtCore.QPointF(x, self.winBox.height() / 2.0)

        # positions and initial settings
        self.vAoBox.moveCenter(self.cen)
        self.vAiBox.moveCenter(self.cen)
        self.cWhBox.moveCenter(self.cen)
        self.vIdBox.moveCenter(self.vIdCen)

        self.cW_rad = self.cWhBox.width() / 2.0
        self.ang_w = radians(self.s_ang) - radians(self.e_ang)

        # gradients
        colWhl = QtGui.QConicalGradient(self.cen, self.o_ang)
        whl_cols = [QtCore.Qt.red, QtCore.Qt.magenta, QtCore.Qt.blue,
                    QtCore.Qt.cyan, QtCore.Qt.green,
                    QtCore.Qt.yellow, QtCore.Qt.red]
        for i, c in enumerate(whl_cols[::self.rot_d]):
            colWhl.setColorAt(i / 6.0, c)

        rad = min(self.cWhBox.width() / 2.0, self.cWhBox.height() / 2.0)
        cWhlFade = QtGui.QRadialGradient(self.cen, rad, self.cen)
        cWhlFade.setColorAt(0, QtCore.Qt.white)
        cWhlFade.setColorAt(1, QtGui.QColor(255, 255, 255, 0))

        self.cWhlBrush1 = QtGui.QBrush(colWhl)
        self.cWhlBrush2 = QtGui.QBrush(cWhlFade)

        # painter paths (arc, wheel)
        rad = self.vAoBox.width() / 2.0
        x, y = rad * cos(radians(self.s_ang)), -rad * sin(radians(self.s_ang))
        x += self.cen.x()
        y += self.cen.y()

        self.vArcPath = QtGui.QPainterPath(QtCore.QPointF(x, y))
        self.vArcPath.arcTo(self.vAoBox, self.s_ang, self.e_ang - self.s_ang)
        self.vArcPath.arcTo(self.vAiBox, self.e_ang, self.s_ang - self.e_ang)
        self.vArcPath.closeSubpath()

        self.colWhlPath = QtGui.QPainterPath()
        self.colWhlPath.addEllipse(self.cWhBox)