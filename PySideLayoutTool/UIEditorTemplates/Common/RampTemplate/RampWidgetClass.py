from __future__ import division

from PySide2 import QtWidgets, QtCore, QtGui
from PySideLayoutTool.UIEditorTemplates.Common.SliderTemplate import SliderWidgetClass
from PySideLayoutTool.UIEditorTemplates.Common.ComboBoxTemplate import ComboBoxWidgetClass
from PySideLayoutTool.UIEditorTemplates.Folder.CollapisbleFolderTemplate import CollapisbleFolderWidgetClass
from PySideLayoutTool.UIEditorTemplates.Common.SeparatorTemplate import SeparatorWidgetClass
from PySideLayoutTool.UIEditorTemplates.Common.LineEditTemplate import LineEditWidgets

from PySideLayoutTool.UIEditorLib import UIEditorIconFactory

import math
from typing import Dict, List, Any, Optional


class RampWidgetSetup(QtWidgets.QWidget):

    def __init__(self, parent):
        super(RampWidgetSetup, self).__init__(parent)
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._parent = parent

        self._init_done = False

        self._widget_buttons = RampWidgetButtons(self)

        self._base_frame = QtWidgets.QGroupBox()

        self._frame_layout = QtWidgets.QVBoxLayout()
        self._frame_layout.setSpacing(0)
        self._frame_layout.setContentsMargins(15, 10, 15, 10)
        self._frame_layout.setAlignment(QtCore.Qt.AlignTop)

        self._ramp_layout = QtWidgets.QVBoxLayout()
        self._ramp_layout.setSpacing(0)
        self._ramp_layout.setAlignment(QtCore.Qt.AlignTop)

        self._collapsible_layout = QtWidgets.QVBoxLayout()
        self._collapsible_layout.setSpacing(0)
        self._collapsible_layout.setContentsMargins(10, 0, 10, 0)
        self._collapsible_layout.setAlignment(QtCore.Qt.AlignTop)

        self._ramp_display = RampGraphicDisplayOuter(self)

        self._slider = RampSliderWidget(self._ramp_display)
        self._slider.baseParent(self)

        self._stack = QtWidgets.QStackedWidget()
        self._itemData = RampWidgetData()

        self._placeholder = QtWidgets.QWidget()
        self._placeholder.setFixedHeight(180)
        self._stack.addWidget(self._placeholder)

        self._collapsible_layout.addWidget(self._stack)
        self._collapsible_folder = CollapisbleFolderWidgetClass.CollapsibleFolderWidget(self._collapsible_layout)
        self._collapsible_folder.folder_title('Controls')
        self._collapsible_folder.open_folder(True)

        self._frame_layout.addWidget(SeparatorWidgetClass.SeparatorHWidget())
        self._frame_layout.addWidget(self._collapsible_folder)

        self._ramp_layout.addWidget(self._ramp_display)
        self._ramp_layout.addLayout(self._frame_layout)

        self._base_frame.setLayout(self._ramp_layout)
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)

        self._layout.addWidget(self._widget_buttons)
        self._layout.addWidget(self._base_frame)
        self.setLayout(self._layout)

        self._init_done = True

    def mapRange_Clamp(self, value, inRangeA, inRangeB, outRangeA, outRangeB):
        if outRangeA == outRangeB: return outRangeA
        if inRangeA == inRangeB: ValueError("inRangeA == inRangeB which will produce one to many mapping")
        inPercentage = (value - inRangeA) / (inRangeB - inRangeA)
        if inPercentage < 0.0: return outRangeA
        if inPercentage > 1.0: return outRangeB
        return outRangeA + inPercentage * (outRangeB - outRangeA)

    def label(self, text: str):
        self._widget_buttons.setLabel(text)

    def bInit(self):
        return self._init_done

    def setbInit(self, state):
        self._init_done = state

    def itemData(self):
        return self._itemData

    def slider_widget(self):
        return self._slider

    def widgetStack(self):
        return self._stack

    def actionButtons(self):
        return self._widget_buttons

    def graphic_scene_outer(self):
        return self._ramp_display

    def graphicScene(self):
        return self._ramp_display.scene

    def update_slider_width(self, width):
        self._slider.updateWidth(width)

    def newHandle(self, position, control):
        return self._slider.newHandle(position, control)

    def newControl(self, index, pos, value, interp):
        if self._placeholder:
            self._stack.removeWidget(self._placeholder)
            self._placeholder = None

        new_control = RampControlsWidget(self)
        new_control.setPosValue(pos)
        new_control.setValue(value)
        new_control.setInterp(interp)

        self._stack.insertWidget(index, new_control)
        self._stack.setCurrentWidget(new_control)

        for i in range(0, self._stack.count()):
            self._stack.widget(i).setMaxNum(self._stack.count())
            self._stack.widget(i).setNum(i + 1)

        return new_control

    def get_ramp(self):
        return self.graphicScene().get_ramp_values()

    def setRamp(self, positions, values, interps):
        scene_height_min = self._ramp_display.ramp().min_height_pos()
        scene_height_max = self._ramp_display.ramp().max_height_pos()

        scene_width_min = self._ramp_display.ramp().min_width_pos()
        scene_width_max = self._ramp_display.ramp().max_width_pos()

        for x in enumerate(positions):
            x_pos = self.mapRange_Clamp(x[1], 0, 1, 0, scene_width_max)
            y_pos = self.mapRange_Clamp(values[x[0]], 0, 1, scene_height_min, 0)
            self._ramp_display.ramp().addRampPoint(x_pos, y_pos, interps[x[0]])


class RampWidgetButtons(QtWidgets.QWidget):

    def __init__(self, parent):
        super(RampWidgetButtons, self).__init__()
        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setSpacing(5)
        self._layout.setContentsMargins(0, 10, 0, 0)
        self._layout.setAlignment(QtCore.Qt.AlignLeft)
        self._parent = parent

        self._label = QtWidgets.QLabel('None')
        self._label.setFixedHeight(20)

        self._spacing_item = QtWidgets.QWidget()
        self._spacing_item.setFixedHeight(15)
        self._spacing_item.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.__open_arrow_icon = UIEditorIconFactory.IconEditorFactory.create('arrow_open')
        self.__close_arrow_icon = UIEditorIconFactory.IconEditorFactory.create('arrow_close')

        self._chart_button = QtWidgets.QPushButton()
        self._chart_button.setFixedSize(20, 20)
        self._chart_button.setFlat(True)
        self._chart_button.setCheckable(True)
        self._chart_button.setIcon(self.__close_arrow_icon)
        self._chart_button.setStyleSheet('QPushButton { background-color: rgba(100, 100, 100, 0); border-radius: 4px; }'
                                         'QPushButton:hover:!pressed{ background-color: #2f2f2f; }'
                                         'QPushButton:flat:checked { background-color: rgba(100, 100, 100, 255); };')

        self._chart_button.toggled.connect(self.update_chart)

        self._rev_domain = QtWidgets.QPushButton()
        self._rev_domain.setFixedSize(20, 20)
        self._rev_domain.setIcon(UIEditorIconFactory.IconEditorFactory.create('arrow_exchange_alt'))
        self._rev_domain.setStyleSheet('QPushButton { background-color: rgba(100, 100, 100, 0); }'
                                       'QPushButton:hover:!pressed{ background-color: #2f2f2f; }'
                                       'QPushButton:pressed{ background-color:  #e1e1e1 };')

        self._rev_domain.pressed.connect(self.reverse_chart)

        self._comp_ramp = QtWidgets.QPushButton()
        self._comp_ramp.setStyleSheet('QPushButton { background-color: rgba(100, 100, 100, 0); }'
                                      'QPushButton:hover:!pressed{ background-color: #2f2f2f; }'
                                      'QPushButton:pressed{ background-color:  #e1e1e1 };')
        self._comp_ramp.setFixedSize(20, 20)
        self._comp_ramp.setIcon(UIEditorIconFactory.IconEditorFactory.create('arrow_exchange_v'))

        self._comp_ramp.pressed.connect(self.comp_chart)

        self._preset_menu = QtWidgets.QPushButton()
        self._preset_menu.setFixedSize(40, 20)
        self._preset_menu.setIcon(UIEditorIconFactory.IconEditorFactory.create('menu_list'))
        self._preset_menu.setStyleSheet('QPushButton { background-color: rgba(100, 100, 100, 0); }'
                                        'QPushButton:hover:!pressed{ background-color: #2f2f2f; }'
                                        'QPushButton:pressed{ background-color:  #e1e1e1 };')

        self.__menu = QtWidgets.QMenu()
        self.__menu.addAction('Constant')
        self.__menu.addAction('Hill')
        self.__menu.addAction('Linear')
        self.__menu.addAction('Round')
        self.__menu.addAction('Sharp')
        self.__menu.addAction('Smooth')
        self.__menu.addAction('Steps')
        self.__menu.addAction('Valley')
        self._preset_menu.setMenu(self.__menu)

        self._type_action = {
            'Constant': self.constantSetup,
            'Hill': self.hillSetup,
            'Linear': self.linearSetup,
            'Round': self.roundSetup,
            'Sharp': self.sharpSetup,
            'Smooth': self.smoothSetup,
            'Steps': self.stepsSetup,
            'Valley': self.valleySetup
        }

        self.__menu.triggered.connect(self.updateRamp)

        self._layout.addWidget(self._label)
        self._layout.addWidget(self._spacing_item)
        self._layout.addWidget(self._chart_button)
        self._layout.addWidget(self._rev_domain)
        self._layout.addWidget(self._comp_ramp)
        self._layout.addWidget(self._preset_menu)

        self.setLayout(self._layout)

    def setLabel(self, text: str):
        self._label.setText(text)

    def updateRamp(self, action):
        func = self._type_action[action.text()]
        self._parent.slider_widget().clearHandles()
        self._parent.graphicScene().clearPoints()
        self._parent.itemData().clear_groups()
        for i in range(0, self._parent.widgetStack().count()):
            self._parent.widgetStack().removeWidget(self._parent.widgetStack().widget(i))
        self._parent.setRamp(*func())

    def update_chart(self, state):
        if state:
            self._chart_button.setIcon(self.__open_arrow_icon)
            self._parent.graphic_scene_outer().set_height(200)
            self._parent.graphicScene().display_grid(True)
            self._parent.graphicScene().scene_collapsed()
            self._parent.slider_widget().update_height(190)
        else:
            self._chart_button.setIcon(self.__close_arrow_icon)
            self._parent.graphic_scene_outer().set_height(50)
            self._parent.graphicScene().display_grid(False)
            self._parent.graphicScene().scene_collapsed()
            self._parent.slider_widget().update_height(40)

    def reverse_chart(self):
        self._parent.graphicScene().reverse_points()

    def comp_chart(self):
        self._parent.graphicScene().complement_points()

    def constantSetup(self):
        return [0], [1], [0]

    def hillSetup(self):
        return [0, 0.5, 1], [0, 1, 0], [5, 5, 5]

    def linearSetup(self):
        return [0, 1], [0, 1], [1, 1]

    def roundSetup(self):
        return [0, 0.8, 1], [0, 0, 1], [4, 4, 4]

    def sharpSetup(self):
        return [0, 0, 1], [0, 1, 1], [4, 4, 4]

    def smoothSetup(self):
        return [0, 1], [0, 1], [3, 3]

    def stepsSetup(self):
        return [0, 0.25, 0.5, 0.75], [0, 0.33, 0.66, 1], [0, 0, 0, 0]

    def valleySetup(self):
        return [0, 0.5, 1], [1, 0, 1], [3, 3, 3]

    def testSetup(self):
        return [0, 0.5, 1], [0, 1, 0.2], [6, 6, 6]


class RampWidgetData:

    def __init__(self):
        super(RampWidgetData, self).__init__()
        self._groupItemA: Dict[Any, List[Any]] = {}
        self._groupItemB: Dict[Any, List[Any]] = {}
        self._groupItemC: Dict[Any, List[Any]] = {}

    def addGroup(self, sceneItem, handle_index, controls) -> None:
        listA = [handle_index, controls]
        self._groupItemA[sceneItem] = listA

        listB = [sceneItem, controls]
        self._groupItemB[handle_index] = listB

        listC = [sceneItem, handle_index]
        self._groupItemC[controls] = listC

    def getGroupA(self) -> Dict:
        return self._groupItemA

    def getGroupB(self) -> Dict:
        return self._groupItemB

    def getGroupC(self) -> Dict:
        return self._groupItemC

    def clear_groups(self):
        self._groupItemA.clear()
        self._groupItemB.clear()
        self._groupItemC.clear()

    def removeGroupItems(self, base_key):
        if base_key in self._groupItemA:
            items = self._groupItemA[base_key]
            self._groupItemA.pop(base_key)
            self._groupItemB.pop(items[0])
            self._groupItemC.pop(items[1])

        elif base_key in self._groupItemB:
            items = self._groupItemB[base_key]
            self._groupItemB.pop(base_key)
            self._groupItemA.pop(items[0])
            self._groupItemC.pop(items[1])

        else:
            items = self._groupItemC[base_key]
            self._groupItemC.pop(base_key)
            self._groupItemA.pop(items[0])
            self._groupItemB.pop(items[1])


class RampSliderWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(RampSliderWidget, self).__init__(parent)
        self.opt = QtWidgets.QStyleOptionSlider()
        self.slider_positions = []
        self._slider_pos_cont = {}

        self.currentIndex = 0
        self._base_parent = None

        self.opt.tickPosition = QtWidgets.QSlider.TicksAbove
        self.opt.minimum = 0
        self.opt.maximum = 1 * 1000000.0

        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed,
                                                 QtWidgets.QSizePolicy.Slider))
        self.move(8, 60)
        self.setFixedWidth(393)

        # Initialize missing attributes
        self._current_handle = None
        self.prev_width = self.rect().width()
        self.initial_width = self.rect().width()

    def baseParent(self, parent):
        self._base_parent = parent

    def handlePosition(self, index):
        return self.slider_positions[index]

    def sort_dict_handles(self):
        self._slider_pos_cont = dict(sorted(self._slider_pos_cont.items(), key=lambda item: item[1]))

    def newHandle(self, position, control):
        self.slider_positions.append(position)
        self._slider_pos_cont[control] = position
        self.sort_dict_handles()
        self.update()
        return len(self.slider_positions) - 1

    def removeHandle(self, index, control):
        self.slider_positions.pop(index)
        self._slider_pos_cont.pop(control)
        self.sort_dict_handles()
        self.update()

    def clearHandles(self):
        self.slider_positions.clear()
        self._slider_pos_cont.clear()
        self.update()

    def handlePositions(self):
        return self.slider_positions

    def handle_dict_positions(self):
        return self._slider_pos_cont

    def updateWidth(self, width):
        self.setFixedWidth(width-7)

    def get_init_pos(self):
        return self.init_pos

    def update_height(self, height):
        self.move(0, height)

    def keyPressEvent(self, event) -> None:
        if event.key() == QtCore.Qt.Key_Backspace or event.key() == QtCore.Qt.Key_Delete:
            itemlist = self._base_parent.itemData().getGroupB()[self.currentIndex]
            self._base_parent.itemData().removeGroupItems(itemlist[1])
            self._base_parent.graphicScene().removePoint(itemlist[0])
            self.removeHandle(self.currentIndex, self._other_parent)
            self._base_parent.widgetStack().removeWidget(itemlist[1])
            itemlist[1].deleteLater()

            for index, i in enumerate(list(self._slider_pos_cont.keys())):
                i.setNum(index + 1)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        # Draw rule
        self.opt.initFrom(self)
        self.opt.rect = self.rect()
        self.opt.sliderPosition = 0
        self.opt.subControls = QtWidgets.QStyle.SC_SliderGroove

        for i in self.slider_positions:
            self.opt.subControls = QtWidgets.QStyle.SC_SliderHandle
            self.opt.sliderPosition = i
            self.style().drawComplexControl(QtWidgets.QStyle.CC_Slider, self.opt, painter)

    def mousePressEvent(self, event):
        distance = self.opt.maximum - self.opt.minimum
        pos = self.style().sliderValueFromPosition(0, distance, event.pos().x(), self.rect().width())

        for i in enumerate(self.slider_positions):
            self.opt.sliderPosition = i[1]
            self.currentIndex = i[0]
            self._current_handle = self.style().hitTestComplexControl(QtWidgets.QStyle.CC_Slider, self.opt, event.pos(),
                                                                      self)

            if math.isclose(pos, i[1], abs_tol=25000):
                itemlist = self._base_parent.itemData().getGroupB()[i[0]]
                if itemlist[0].parentScene().currentSelected() != itemlist[0]:
                    itemlist[0].parentScene().itemSelect(itemlist[0])

                self._current_control = itemlist[1]
                self._base_parent.widgetStack().setCurrentWidget(self._current_control)
                return

    def mouseMoveEvent(self, event):
        distance = self.opt.maximum - self.opt.minimum
        pos = self.style().sliderValueFromPosition(0, distance, event.pos().x(), self.rect().width())

        if self._current_handle == QtWidgets.QStyle.SC_SliderHandle:
            self.slider_positions[self.currentIndex] = pos
            self._slider_pos_cont[self._current_control] = pos
            self.sort_dict_handles()

            itemlist = self._base_parent.itemData().getGroupB()[self.currentIndex]
            itemlist[1].setPosValue(self._base_parent.mapRange_Clamp(pos, 0, 1000000.0, 0, 1))
            itemlist[0].parentScene().moveXItem(itemlist[0], pos)
            itemlist[0].parentScene().drawPath()

            for index, i in enumerate(list(self._slider_pos_cont.keys())):
                i.setNum(index + 1)

            self.update()
            return

    def moveSlider(self, index, control, pos):
        self.slider_positions[index] = pos
        self._slider_pos_cont[control] = pos
        self.update()


class PointNumWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(PointNumWidget, self).__init__()
        self._parent = parent
        self._other_parent = None
        self._base_index = 0
        self._current_index = 1

        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 5, 0, 5)
        self._layout.setAlignment(QtCore.Qt.AlignLeft)

        self._index_widget = LineEditWidgets.LineEditIntWidgetClass(no_num_button=False, parent=self)
        self._index_widget.base_widget().setToolTip('Mouse wheel to change Selection.')
        self._index_widget.base_widget().setStyleSheet(
            "QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")

        self._add_button = QtWidgets.QPushButton('+')
        self._add_button.setFont(QtGui.QFont('+', 8, QtGui.QFont.Bold))
        self._add_button.setFixedWidth(25)
        self._add_button.setProperty('class', 'add_button')

        self._sub_button = QtWidgets.QPushButton('-')
        self._sub_button.setFont(QtGui.QFont('-', 12, QtGui.QFont.Bold))
        self._sub_button.setFixedWidth(25)
        self._sub_button.setProperty('class', 'sub_button')

        self._layout.addWidget(self._index_widget)
        self._layout.addSpacing(5)
        self._layout.addWidget(SeparatorWidgetClass.SeparatorVWidget())
        self._layout.addSpacing(5)
        self._layout.addWidget(self._add_button)
        self._layout.addSpacing(1)
        self._layout.addWidget(self._sub_button)

        self.setFixedHeight(40)

        self.setLayout(self._layout)

        self._add_button.pressed.connect(self.add_point)
        self._sub_button.pressed.connect(self.remove_point)
        self._index_widget.base_widget().valueChanged.connect(self.updateSelection)

    def controllerParent(self):
        return self._other_parent

    def setControllerParent(self, parent):
        self._other_parent = parent

    def setBase(self, value):
        self._base_index = value
        self._index_widget.setValue(value)

    def setRange(self, maxValue):
        self._index_widget.setRange(1, maxValue)

    def updateSelection(self, value):
        if self._parent.bInit():
            self._parent.setbInit(False)
            controls = list(self._parent.slider_widget().handle_dict_positions().keys())
            self._parent.widgetStack().setCurrentWidget(controls[value - 1])
            itemlist = self._parent.itemData().getGroupC()[controls[value - 1]]
            itemlist[0].parentScene().itemSelect(itemlist[0])
            self._index_widget.setValue(self._base_index)
            self.setFocus()
            self._parent.setbInit(True)

    def add_point(self):
        itemlist = self._parent.itemData().getGroupC()[self._other_parent]
        self._parent.graphicScene().insert_point(itemlist[0])

    def remove_point(self):
        itemlist = self._parent.itemData().getGroupC()[self._other_parent]
        self._parent.itemData().removeGroupItems(self._other_parent)
        self._parent.graphicScene().removePoint(itemlist[0])
        self._parent.slider_widget().removeHandle(itemlist[1], self._other_parent)
        self._parent.widgetStack().removeWidget(self._other_parent)
        self._other_parent.deleteLater()

        for index, i in enumerate(list(self._parent.slider_widget().handle_dict_positions().keys())):
            i.setNum(index + 1)


class RampControlsWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(RampControlsWidget, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setAlignment(QtCore.Qt.AlignTop)
        self._parent = parent

        self._sliderChange = True
        self._notSelf = False
        self._base_num = 0

        self._num_widget = PointNumWidget(parent)
        self._num_widget.setControllerParent(self)

        self._pos_slider = SliderWidgetClass.FloatSliderWidget()
        self._pos_slider.setRange(0, 1 * 1000000.0)

        self._val_slider = SliderWidgetClass.FloatSliderWidget()
        self._val_slider.setRange(0, 1 * 1000000.0)

        self._menu_interp = ComboBoxWidgetClass.ComboBoxWidget()
        self._menu_interp.addItems(
            ['Constant', 'Linear', 'Catmull-Rom', 'Monotone-Cubic', 'Bezier', 'B-Spline', 'Hermite'])

        self.withLabel('Point No.', self._num_widget)
        self.withLabel('Position', self._pos_slider)
        self.withLabel('Value', self._val_slider)
        self.withLabel('Interpolation', self._menu_interp)

        self.setLayout(self._layout)

        self._pos_slider.slider.valueChanged.connect(self.updatePosition)
        self._val_slider.slider.valueChanged.connect(self.updateValue)

        self._menu_interp._combo_box.activated.connect(self.updatePath)

    def withLabel(self, text, widget_obj):
        hor_layout = QtWidgets.QHBoxLayout()
        hor_layout.setSpacing(5)
        hor_layout.setContentsMargins(0, 0, 0, 0)

        hor_layout.addWidget(QtWidgets.QLabel(text=text))
        hor_layout.addWidget(widget_obj)

        self._layout.addLayout(hor_layout)

    def updatePath(self, index):
        itemlist = self._parent.itemData().getGroupC()[self]
        self._parent.graphicScene().updateInterp(itemlist[0], index)
        self._parent.graphicScene().drawPath()

    def changeSelection(self, value):
        if self._notSelf:
            self._parent.widgetStack().setCurrentIndex(value - 1)
            other = self._parent.widgetStack().currentWidget()
            itemlist = self._parent.itemData().getGroupC()[other]
            itemlist[0].parentScene().itemSelect(itemlist[0])
            self.setNum(self._base_num)

    def updatePosition(self, value):
        if self._parent.bInit():
            value = self._parent.mapRange_Clamp(value, 0, 1000000.0, 0, 1000000.0)
            itemlist = self._parent.itemData().getGroupC()[self]
            self._parent.slider_widget().moveSlider(itemlist[1], self, value)
            itemlist[0].parentScene().moveXItem(itemlist[0], value)
            itemlist[0].parentScene().drawPath()

            self._parent.slider_widget().sort_dict_handles()

            for index, i in enumerate(list(self._parent.slider_widget().handle_dict_positions().keys())):
                i.setNum(index + 1)

    def updateValue(self, value):
        if self._parent.bInit():
            itemlist = self._parent.itemData().getGroupC()[self]
            itemlist[0].parentScene().moveYItem(itemlist[0], value)
            itemlist[0].parentScene().drawPath()

    def number(self):
        return self._num_widget._index_widget.value()

    def setNum(self, number: int):
        self._num_widget.setBase(number)

    def setMaxNum(self, max_num: int):
        self._num_widget.setRange(max_num)

    def setPosValue(self, position: float):
        self._pos_slider.setValue(position)

    def setValue(self, value: float):
        self._val_slider.setValue(value)

    def setInterp(self, index: int):
        self._menu_interp.setItem(index)


class RampGraphicDisplayOuter(QtWidgets.QWidget):

    def __init__(self, parent):
        super(RampGraphicDisplayOuter, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(5, 0, 5, 10)
        self._display_height = 75
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self._parent = parent
        self.setFixedHeight(self._display_height + 15)

        self.scene = RampGraphicScene(self)

        self.view = QtWidgets.QGraphicsView(self.scene)

        self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.view.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        self.view.setRenderHint(QtGui.QPainter.TextAntialiasing)
        self.view.setOptimizationFlag(QtWidgets.QGraphicsView.DontAdjustForAntialiasing, True)
        self.view.setOptimizationFlag(QtWidgets.QGraphicsView.DontSavePainterState, True)
        self.view.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.view.setOptimizationFlag(QtWidgets.QGraphicsView.IndirectPainting)

        self.view.setViewportMargins(0, 0, 0, 0)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.transparent))
        self.view.setStyleSheet("border: transparent;")

        self._layout.addWidget(self.view)
        self.setLayout(self._layout)

    def resizeEvent(self, event):
        super(RampGraphicDisplayOuter, self).resizeEvent(event)
        self.adjust_scene_rect()
        self.scene.update_scene()

    def adjust_scene_rect(self):
        padding = 9
        new_scene_rect = QtCore.QRectF(padding, padding, self.view.width() - 2 * padding,
                                       self._display_height - 2 * padding)
        self.scene.setSceneRect(new_scene_rect)
        self.scene.bounding_rect = new_scene_rect
        self.scene.update()
        self._parent.update_slider_width(self.view.width())

    def ramp(self):
        return self.scene

    def set_height(self, height):
        self._display_height = height + 15
        self._ramp_display.set_view_height(height)
        self.setFixedHeight(self._display_height)


class CustomEllipseItem(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, x, y, w, h, scene, parent=None):
        super(CustomEllipseItem, self).__init__(x, y, w, h, parent)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self._scene = scene

    def mouseMoveEvent(self, event):
        new_pos = event.scenePos()
        bound_rect = self._scene.bounding_rect
        item_width = self.rect().width()
        item_height = self.rect().height()

        # Check if the ellipse's position stays inside the white rectangle
        if (bound_rect.left() <= new_pos.x() <= (bound_rect.right() + 6) - item_width and
                bound_rect.top() <= new_pos.y() <= (bound_rect.bottom() + 6) - item_height):
            super(CustomEllipseItem, self).mouseMoveEvent(event)
            self._scene.update_values(self)

    def parentScene(self):
        return self._scene


class RampGraphicScene(QtWidgets.QGraphicsScene):

    def __init__(self, parent):
        super(RampGraphicScene, self).__init__()
        self._parent = parent
        self.setSceneRect(0, 0, 300, 50)
        self.bounding_rect = QtCore.QRectF()

        self.width_min = 0
        self.width_max = 0

        self.__doOnce = True
        self._show_grid = False

        self.points = []
        self.interps = {}
        self.ellipse_items = []

        self.xLines = []
        self.yLines = []
        self.xText = []
        self.yText = []

        self.scenePath = None
        self.lastPoint = None
        self.currentPoint = None
        self._mouseState = False

        # self.updateGridY()

    def drawForeground(self, painter, rect):
        super(RampGraphicScene, self).drawForeground(painter, rect)

        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(45, 45, 45)))  # 50% opacity
        painter.drawRect(self.bounding_rect)

        if self.scenePath:
            painter.setBrush(self.scenePath.brush())
            painter.drawPath(self.scenePath.path())

        # Draw items above white rectangle
        if self._parent is not None:
            for i in self.ellipse_items:
                painter.setBrush(i.brush())
                painter.setPen(i.pen())
                painter.drawEllipse(i.sceneBoundingRect())

    def keyPressEvent(self, event) -> None:
        if event.key() == QtCore.Qt.Key_Backspace or event.key() == QtCore.Qt.Key_Delete:
            itemlist = self._parent._parent.itemData().getGroupA()[self.currentPoint]
            self._parent._parent.itemData().removeGroupItems(itemlist[1])
            self.removePoint(self.currentPoint)
            self._parent._parent.slider_widget().removeHandle(itemlist[0], itemlist[1])
            self._parent._parent.widgetStack().removeWidget(itemlist[1])
            itemlist[1].deleteLater()

            for index, i in enumerate(list(self._parent._parent.slider_widget().handle_dict_positions().keys())):
                i.setNum(index + 1)

    def min_height_pos(self):
        return self.bounding_rect.bottom() - 10

    def max_height_pos(self):
        return 0

    def min_width_pos(self):
        return 0

    def max_width_pos(self):
        return self.bounding_rect.right() - 10

    def scene_collapsed(self):
        self._y_min = 180 if self._show_grid else 30.0

        for p in self.points:
            newPos = self._parent._parent.mapRange_Clamp(p.pos().y(), 30.0 if self._show_grid else 180.0, self._y_max,
                                                         self._y_min, self._y_max)
            p.setPos(p.pos().x(), newPos)

    def display_grid(self, state: bool):
        self._show_grid = state

        for x in self.xLines:
            x.setVisible(state)

        for y in self.yLines:
            y.setVisible(state)

        for tx in self.xText:
            tx.setVisible(state)

        for ty in self.yText:
            ty.setVisible(state)

    def reverse_points(self):
        for p in self.points:
            new_x_pos = self._parent._parent.mapRange_Clamp(p.pos().x(), self._min, self.width - self._sub,
                                                            self.width - self._sub, self._min)
            p.setPos(new_x_pos, p.pos().y())
            self.sortPoints()
            self.update_values(p)

        for index, sort_p in enumerate(self.points):
            data_item = self._parent._parent.itemData().getGroupA()[sort_p]
            data_item[1].setNum(index + 1)

    def complement_points(self):
        for p in self.points:
            new_y_pos = self._parent._parent.mapRange_Clamp(p.pos().y(), self._y_min, self._y_max, self._y_max,
                                                            self._y_min)
            p.setPos(p.pos().x(), new_y_pos)
            self.update_values(p)

    def update_scene(self):
        # self.updateGridX()
        if self.__doOnce:
            self.__doOnce = False
            if len(self.points) <= 0:
                self._parent._parent.setRamp(*self._parent._parent.actionButtons().linearSetup())
        else:
            self.updatePoints()
            self.drawPath()

    def mousePressEvent(self, event) -> None:
        pos = event.scenePos()
        item = self.itemAt(pos, QtGui.QTransform())

        if isinstance(item, CustomEllipseItem):
            if self.selectedItems()[0] != item:
                self.itemSelect(item)
                itemlist = self._parent._parent.itemData().getGroupA()[item]
                self._parent._parent.widgetStack().setCurrentWidget(itemlist[1])
                return
            else:
                self._mouseState = True
                super(RampGraphicScene, self).mousePressEvent(event)
                return
        else:
            pos.setX(pos.x() - 8)
            pos.setY(pos.y() - 8)
            self.addNew_EllipsePoint(pos, self.interps[self.lastPoint])
            return

    def mouseReleaseEvent(self, event) -> None:
        super(RampGraphicScene, self).mouseReleaseEvent(event)
        self._mouseState = False

    def updateGridX(self):
        line_pen = QtGui.QPen(QtGui.QColor(80, 80, 80), 1, QtCore.Qt.SolidLine)
        text_color = QtGui.QColor(80, 80, 80)
        x_text = []

        if 600 <= self.width < 1500:
            num = 0
            x_text = []
            for i in range(0, 19):
                num += 0.05
                x_text.append(str(round(num, 3)))

        elif self.width >= 1500:
            num = 0
            x_text = []
            for i in range(0, 49):
                num += 0.02
                x_text.append(str(round(num, 3)))
        else:
            num = 0
            x_text = []
            for i in range(0, 9):
                num += 0.1
                x_text.append(str(round(num, 3)))

        divLen = len(x_text) + 1
        bottom = 170
        xpos = (abs(self._min) + (self.width - 148)) / divLen - abs(self._min)

        if len(self.xLines) != 0:
            for i in range(0, len(self.xLines)):
                self.removeItem(self.xLines[i])
                self.removeItem(self.xText[i])

            self.xLines.clear()
            self.xText.clear()

        for i in range(0, len(x_text)):
            text_item = self.addText(x_text[i], QtGui.QFont(x_text[i], 8, QtGui.QFont.Normal))
            text_item.setDefaultTextColor(text_color)
            text_item.setPos(xpos - 4, bottom)

            new_line = self.addLine(xpos + 10, -100, xpos + 10, bottom, line_pen)
            self.xLines.append(new_line)
            self.xText.append(text_item)

            new_line.setVisible(self._show_grid)
            text_item.setVisible(self._show_grid)

            xpos += (self.width - 4) / divLen

    def updateGridY(self):
        line_pen = QtGui.QPen(QtGui.QColor(80, 80, 80), 1, QtCore.Qt.SolidLine)
        text_color = QtGui.QColor(80, 80, 80)

        ypos = 140  # 64 old
        y_text = ['0.2', '0.4', '0.6', '0.8']

        for i in range(0, len(y_text)):
            text_item = self.addText(y_text[i], QtGui.QFont(y_text[i], 8, QtGui.QFont.Normal))
            text_item.setDefaultTextColor(text_color)
            text_item.setPos(-138.0, ypos)

            new_line = self.addLine(-115.0, ypos + 10, 10000, ypos + 10, line_pen)
            new_line.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations)
            self.yLines.append(new_line)
            self.yText.append(text_item)

            new_line.setVisible(self._show_grid)
            text_item.setVisible(self._show_grid)

            ypos -= 39

    def currentSelected(self):
        return self.currentPoint

    def itemSelect(self, item):
        item.setSelected(True)
        item.setBrush(QtGui.QColor(0, 205, 255))

        if self.lastPoint is not None:
            self.lastPoint.setBrush(QtGui.QColor(0, 0, 0))
            self.lastPoint.setSelected(False)

        self.currentPoint = item
        self.lastPoint = item

    def removePoint(self, item):
        self.removeItem(item)
        index = self.points.index(item)
        new_index = 0
        if index + 1 == len(self.points):
            new_index = index - 1

        elif index + 1 < len(self.points):
            new_index = index + 1

        self.itemSelect(self.points[new_index])
        self.points.pop(index)
        self.drawPath()

    def clearPoints(self):
        for p in self.points:
            self.removeItem(p)

        self.points.clear()

    def insert_point(self, point):
        index = self.points.index(point)
        next_point = self.points[index + 1] if index < (len(self.points) - 1) else self.points[index - 1]
        x_pos = (point.pos().x() + next_point.pos().x()) / 2
        y_pos = (point.pos().y() + next_point.pos().y()) / 2
        interp = self.interps[point]
        position = QtCore.QPointF(x_pos, y_pos)
        self.addNew_EllipsePoint(position, interp)

    def get_ramp_values(self):
        points_pos = []
        points_value = []
        for p in self.points:
            points_pos.append(
                self._parent._parent.mapRange_Clamp(p.pos().x(), self.min_width_pos(), self.max_width_pos(), 0, 1))
            points_value.append(
                self._parent._parent.mapRange_Clamp(p.pos().y(), self.min_height_pos(), self.max_height_pos(), 0, 1))

        return {'positions': points_pos, 'values': points_value, 'interpolations': list(self.interps.values())}

    def addRampPoint(self, pos, value, interp):
        position = QtCore.QPointF(pos, value)
        self.addNew_EllipsePoint(position, interp)

    def addNew_EllipsePoint(self, position, interp=0):
        self._parent._parent.setbInit(False)

        newEllipse = CustomEllipseItem(5, 5, 8, 8, self)
        newEllipse.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 2, QtCore.Qt.SolidLine))
        newEllipse.setBrush(QtGui.QBrush(QtGui.QColor(0, 205, 255)))
        newEllipse.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable | QtWidgets.QGraphicsItem.ItemIsSelectable)
        newEllipse.setPos(position)
        newEllipse.setSelected(True)
        newEllipse.setZValue(1)

        self.ellipse_items.append(newEllipse)

        self.addItem(newEllipse)
        self.points.append(newEllipse)
        self.sortPoints()
        self.interps[newEllipse] = interp

        slider_pos = self._parent._parent.mapRange_Clamp(position.x(), self.min_width_pos(), self.max_width_pos(),
                                                         0, 1000000.0)
        control_x_pos = self._parent._parent.mapRange_Clamp(position.x(), self.min_width_pos(), self.max_width_pos(), 0,
                                                            1)
        control_y_pos = self._parent._parent.mapRange_Clamp(position.y(), self.min_height_pos(), self.max_height_pos(),
                                                            0, 1)

        control_widget = self._parent._parent.newControl(self.points.index(newEllipse), control_x_pos, control_y_pos,
                                                         interp)
        slider_index = self._parent._parent.newHandle(int(slider_pos), control_widget)
        self._parent._parent.itemData().addGroup(newEllipse, slider_index, control_widget)

        self.itemSelect(newEllipse)
        self.drawPath()
        self._parent._parent.setbInit(True)

    def sortPoints(self):
        positions = []
        for i in self.points:
            positions.append(i.pos().x())

        pos_sorted = sorted(positions)
        points_sorted = []
        for i in range(0, len(pos_sorted)):
            current_point_pos = self.points[i].pos().x()
            index = pos_sorted.index(current_point_pos)
            points_sorted.insert(index, self.points[i])

        self.points = points_sorted

    def updatePoints(self):
        for i in self.points:
            itemlist = self._parent._parent.itemData().getGroupA()[i]
            pos = self._parent._parent.slider_widget().handlePosition(itemlist[0])
            newPos = self._parent._parent.mapRange_Clamp(pos, 0, 1000000.0, self.min_width_pos(),
                                                         self.max_width_pos())
            i.setPos(newPos, i.pos().y())

    def updateInterp(self, item, index):
        self.interps[item] = index

    def update_values(self, item):
        itemlist = self._parent._parent.itemData().getGroupA()[item]

        slider_pos = self._parent._parent.mapRange_Clamp(item.pos().x(), self.min_width_pos(), self.max_width_pos(),
                                                         0, 1000000.0)
        self._parent._parent.slider_widget().moveSlider(itemlist[0], itemlist[1], slider_pos)

        control_x_pos = self._parent._parent.mapRange_Clamp(item.pos().x(), self.min_width_pos(), self.max_width_pos(),
                                                            0, 1)
        control_y_pos = self._parent._parent.mapRange_Clamp(item.pos().y(), self.min_height_pos(),
                                                            self.max_height_pos(), 0, 1)

        itemlist[1].setPosValue(control_x_pos)
        itemlist[1].setValue(control_y_pos)

        self._parent._parent.slider_widget().sort_dict_handles()
        self.sortPoints()

        for index, i in enumerate(list(self._parent._parent.slider_widget().handle_dict_positions().keys())):
            i.setNum(index + 1)

        self.drawPath()

    def moveXItem(self, item, pos_x):
        pos_x = self._parent._parent.mapRange_Clamp(pos_x, 0, 1000000.0, self.min_width_pos(), self.max_width_pos())
        item.setPos(pos_x, item.pos().y())
        self.sortPoints()

    def moveYItem(self, item, pos_y):
        pos_y = self._parent._parent.mapRange_Clamp(pos_y, 0, 1000000.0, self.min_height_pos(), self.max_height_pos())
        item.setPos(item.pos().x(), pos_y)

    def drawPath(self):
        if self.scenePath:
            self.removeItem(self.scenePath)
            self.scenePath = None

        rect_item_path = QtGui.QPainterPath()
        rect_item_path.addRect(self.bounding_rect)

        addition = 10
        path = QtGui.QPainterPath()
        path.moveTo(-160, 250)
        path.lineTo(-160, self.points[0].pos().y() + addition)

        blend_overlap = 5  # Number of overlapping points between segments to blend

        i = 0
        while i < len(self.points):
            p = self.points[i]
            interp = self.interps[p]

            if interp == 0:  # Constant
                path.lineTo(p.pos().x() + addition, p.pos().y() + addition)
                if p != self.points[-1]:
                    path.lineTo(self.points[i + 1].pos().x() + addition, p.pos().y() + addition)

            elif interp == 1:  # Linear
                path.lineTo(p.pos().x() + addition, p.pos().y() + addition)

            else:
                pts = [(ip.pos().x() + addition, ip.pos().y() + addition) for ip in self.points[i:] if
                       self.interps[ip] == interp]

                curve_points = []

                if interp == 2:  # Catmull-Rom
                    if len(pts) >= 4:
                        curve_points = catmull_rom_chain(pts, 100)

                elif interp == 3:  # Monotone Cubic
                    if len(pts) >= 2:
                        pts_x = [p[0] for p in pts]
                        pts_y = [p[1] for p in pts]
                        curve_points = monotone_cubic_interpolation(pts_x, pts_y)

                elif interp == 4:  # Bezier
                    if len(pts) >= 4:
                        curve_points = bezier_curve(pts, 100)

                elif interp == 5:  # B-Spline
                    if len(pts) >= 4:
                        curve_points = bspline_interpolation(pts, 100)

                elif interp == 6:  # Hermite
                    if len(pts) >= 2:
                        curve_points = hermite_interpolation(pts, 100)

                if curve_points:
                    if i + 1 < len(self.points):
                        next_interp = self.interps[self.points[i + 1]]
                        if interp != next_interp and next_interp not in [0, 1]:
                            next_pts = [(ip.pos().x() + addition, ip.pos().y() + addition) for ip in self.points[i + 1:]
                                        if
                                        self.interps[ip] == next_interp]

                            next_curve_points = []  # Initialize next_curve_points as an empty list
                            if len(next_pts) >= 2:
                                if next_interp == 2:  # Catmull-Rom
                                    if len(next_pts) >= 4:
                                        next_curve_points = catmull_rom_chain(next_pts, 100)

                                elif next_interp == 3:  # Monotone Cubic
                                    next_pts_x = [p[0] for p in next_pts]
                                    next_pts_y = [p[1] for p in next_pts]
                                    next_curve_points = monotone_cubic_interpolation(next_pts_x, next_pts_y)

                                elif next_interp == 4:  # Bezier
                                    if len(next_pts) >= 4:
                                        next_curve_points = bezier_curve(next_pts, 100)

                                elif next_interp == 5:  # B-Spline
                                    if len(next_pts) >= 4:
                                        next_curve_points = bspline_interpolation(next_pts, 100)

                                elif next_interp == 6:  # Hermite
                                    if len(next_pts) >= 2:
                                        next_curve_points = hermite_interpolation(next_pts, 100)

                                if next_curve_points:
                                    blend_start = curve_points[-blend_overlap:]
                                    blend_end = next_curve_points[:blend_overlap]
                                    blended_segment = blend_segments(blend_start, blend_end)

                                    curve_points = curve_points[:-blend_overlap] + blended_segment + next_curve_points[
                                                                                                     blend_overlap:]

                    for point in curve_points:
                        path.lineTo(point[0], point[1])

                    i += len(pts) - 1

            i += 1

        distance = self.max_width_pos() - self.points[-1].pos().x()
        path.lineTo(self.points[-1].pos().x() + abs(distance) + 30,
                    self.points[-1].pos().y() + addition)
        path.lineTo(self.points[-1].pos().x() + abs(distance) + 30, 250.0)

        clipped_path = path.intersected(rect_item_path)
        self.scenePath = self.addPath(clipped_path, QtGui.QPen(QtGui.QColor(25, 25, 25, 125), 3,
                                                               QtCore.Qt.SolidLine),
                                      QtGui.QBrush(QtGui.QColor(200, 200, 200, 125)))


class GraphicSceneMediator(QtCore.QObject):

    def __init__(self, scene1, scene2):
        super(GraphicSceneMediator, self).__init__()
        self._scene1 = scene1
        self._scene1.mediator = self
        self._scene2 = scene2
        self._scene2.mediator = self

    def update_points(self, points):
        self._scene2.update_points(points)

    def update_path(self):
        self._scene2.draw_path()


class SceneMediator:
    """
    The Base Component provides the basic functionality of storing a mediator's
    instance inside component objects.
    """

    def __init__(self, mediator=None) -> None:
        self._mediator = mediator

    @property
    def mediator(self):
        return self._mediator

    @mediator.setter
    def mediator(self, mediator) -> None:
        self._mediator = mediator


def blend_segments(segment1, segment2, blend_factor=0.5):
    blended = []
    for i in range(len(segment1)):
        blended_x = segment1[i][0] * (1 - blend_factor) + segment2[i][0] * blend_factor
        blended_y = segment1[i][1] * (1 - blend_factor) + segment2[i][1] * blend_factor
        blended.append((blended_x, blended_y))
    return blended


# Add these functions outside the class
def lerp(a, b, t):
    return a * (1 - t) + b * t


def catmull_rom_spline(points, samples_per_segment):
    def catmull_rom(p0, p1, p2, p3, t):
        return (
                0.5 * (
                (2 * p1)
                + (-p0 + p2) * t
                + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3
        )
        )

    result = []
    for i in range(len(points) - 3):
        for t in range(samples_per_segment):
            tt = t / samples_per_segment
            x = catmull_rom(points[i][0], points[i + 1][0], points[i + 2][0], points[i + 3][0], tt)
            y = catmull_rom(points[i][1], points[i + 1][1], points[i + 2][1], points[i + 3][1], tt)
            result.append((x, y))

    return result


def catmull_rom_chain(points, num_points, tension=0.5):
    def catmull_rom(p0, p1, p2, p3, t, tension):
        t2 = t * t
        t3 = t2 * t
        a1 = (tension * (p2[0] - p0[0]), tension * (p2[1] - p0[1]))
        a2 = (tension * (p3[0] - p1[0]), tension * (p3[1] - p1[1]))

        return (
            0.5 * (
                    (2 * p1[0])
                    + (-p0[0] + p2[0]) * t
                    + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                    + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3
            ),
            0.5 * (
                    (2 * p1[1])
                    + (-p0[1] + p2[1]) * t
                    + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                    + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3
            ),
        )

    extra_start_pt = (points[0][0] - 10, points[0][1])
    extra_end_pt = (points[-1][0] + 10, points[-1][1])

    points.insert(0, extra_start_pt)
    points.append(extra_end_pt)

    catmull_rom_points = []

    for i in range(len(points) - 3):
        p0, p1, p2, p3 = points[i], points[i + 1], points[i + 2], points[i + 3]

        for j in range(num_points + 1):
            t = j / num_points
            catmull_rom_points.append(catmull_rom(p0, p1, p2, p3, t, tension))

    return catmull_rom_points


# def catmull_rom_chain(points, num_points, tension=0.5):
#     def catmull_rom(p0, p1, p2, p3, t, tension):
#         t2 = t * t
#         t3 = t2 * t
#         a1 = (tension * (p2[0] - p0[0]), tension * (p2[1] - p0[1]))
#         a2 = (tension * (p3[0] - p1[0]), tension * (p3[1] - p1[1]))
#
#         return (
#             0.5 * (
#                 (2 * p1[0])
#                 + (-p0[0] + p2[0]) * t
#                 + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
#                 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3
#             ),
#             0.5 * (
#                 (2 * p1[1])
#                 + (-p0[1] + p2[1]) * t
#                 + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
#                 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3
#             ),
#         )
#
#     num_segments = len(points) - 3
#     curve_points = []
#
#     if num_segments == 1:
#         for i in range(num_points):
#             t = i / float(num_points)
#             curve_points.append(catmull_rom(points[0], points[1], points[2], points[3], t, tension))
#     else:
#         for i in range(num_segments):
#             p0, p1, p2, p3 = points[i : i + 4]
#             for j in range(num_points):
#                 t = j / float(num_points)
#                 curve_points.append(catmull_rom(p0, p1, p2, p3, t, tension))
#
#     return curve_points

def monotone_cubic_interpolation(x, y):
    n = len(x)
    delta = [0.0] * (n - 1)
    m = [0.0] * n

    for i in range(n - 1):
        if x[i + 1] - x[i] != 0:
            delta[i] = (y[i + 1] - y[i]) / (x[i + 1] - x[i])
        else:
            delta[i] = 0.0

    if n > 2:
        m[0] = delta[0]
        m[n - 1] = delta[n - 2]

    for i in range(1, n - 1):
        if delta[i - 1] * delta[i] <= 0:
            m[i] = 0
        else:
            m[i] = (delta[i - 1] + delta[i]) / 2

    result = []

    for i in range(n - 1):
        t = [j / 100 for j in range(101)]
        a = y[i]
        b = m[i]
        c = 3 * delta[i] - 2 * m[i] - m[i + 1]
        d = m[i] + m[i + 1] - 2 * delta[i]

        for tt in t:
            yy = a + b * (x[i + 1] - x[i]) * tt + c * (x[i + 1] - x[i]) * tt ** 2 + d * (x[i + 1] - x[i]) * tt ** 3
            xx = lerp(x[i], x[i + 1], tt)
            result.append((xx, yy))

    return result


def de_casteljau(points, t):
    if len(points) == 1:
        return points[0]
    else:
        new_points = []
        for i in range(len(points) - 1):
            x = (1 - t) * points[i][0] + t * points[i + 1][0]
            y = (1 - t) * points[i][1] + t * points[i + 1][1]
            new_points.append((x, y))
        return de_casteljau(new_points, t)


def bezier_curve(points, num_points):
    curve = []
    for i in range(num_points + 1):
        t = i / num_points
        curve.append(de_casteljau(points, t))
    return curve


def cox_de_boor(t, i, k, knots):
    if k == 1:
        if knots[i] <= t < knots[i + 1]:
            return 1
        else:
            return 0
    else:
        a = ((t - knots[i]) * cox_de_boor(t, i, k - 1, knots)) / (knots[i + k - 1] - knots[i]) if knots[i + k - 1] != \
                                                                                                  knots[i] else 0
        b = ((knots[i + k] - t) * cox_de_boor(t, i + 1, k - 1, knots)) / (knots[i + k] - knots[i + 1]) if knots[
                                                                                                              i + k] != \
                                                                                                          knots[
                                                                                                              i + 1] else 0
        return a + b


def bspline_interpolation(points, num_points, degree=3):
    num_knots = len(points) + degree + 1
    knots = [0] * (degree + 1) + list(range(1, num_knots - 2 * (degree + 1) + 1)) + [num_knots - degree] * (degree + 1)
    curve = []
    for i in range(num_points + 1):
        t = i / num_points * (num_knots - 2 * (degree + 1))
        x, y = 0, 0
        for i, point in enumerate(points):
            b = cox_de_boor(t, i, degree + 1, knots)
            x += b * point[0]
            y += b * point[1]
        curve.append((x, y))
    return curve


def hermite_interpolation(points, num_points, tangents=None):
    if tangents is None:
        tangents = [(points[i + 1][0] - points[i - 1][0], points[i + 1][1] - points[i - 1][1]) for i in
                    range(1, len(points) - 1)]
        tangents.insert(0, (points[1][0] - points[0][0], points[1][1] - points[0][1]))
        tangents.append((points[-1][0] - points[-2][0], points[-1][1] - points[-2][1]))

    curve = []
    for i in range(len(points) - 1):
        p0, p1 = points[i], points[i + 1]
        m0, m1 = tangents[i], tangents[i + 1]

        for j in range(num_points + 1):
            t = j / num_points
            t2 = t * t
            t3 = t2 * t

            h00 = 2 * t3 - 3 * t2 + 1
            h10 = -2 * t3 + 3 * t2
            h01 = t3 - 2 * t2 + t
            h11 = t3 - t2

            x = h00 * p0[0] + h10 * p1[0] + h01 * m0[0] + h11 * m1[0]
            y = h00 * p0[1] + h10 * p1[1] + h01 * m0[1] + h11 * m1[1]

            curve.append((x, y))

    return curve
