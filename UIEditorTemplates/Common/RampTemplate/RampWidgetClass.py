
from __future__ import division
from functools import reduce
from operator import mul
# import numpy as np


from PySide2 import QtWidgets, QtCore, QtGui
from PySideLayoutTool.UIEditorTemplates.Common.SliderTemplate import SliderWidgetClass
from PySideLayoutTool.UIEditorTemplates.Common.ComboBoxTemplate import ComboBoxWidgetClass
from PySideLayoutTool.UIEditorTemplates.Folder.CollapisbleFolderTemplate import CollapisbleFolderWidgetClass
from PySideLayoutTool.UIEditorTemplates.Common.SeparatorTemplate import SeparatorWidgetClass
from PySideLayoutTool.UIEditorTemplates.Common.LineEditTemplate import LineEditWidgets

from PySideLayoutTool.UIEditorLib import UIEditorIconFactory

import math
from typing import Dict, List, Any


#TODO: FIX!!! Resize on init.
# reOrder points on x position when moved and redraw curve.
# Implement curve interpolations.


class RampWidgetSetup(QtWidgets.QWidget):

    def __init__(self,parent):
        super(RampWidgetSetup, self).__init__(parent)
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0,0,0,0)
        self._parent = parent

        self._init_done = False

        self._widget_buttons = RampWidgetButtons(self)

        self._base_frame = QtWidgets.QGroupBox()

        self._frame_layout = QtWidgets.QVBoxLayout()
        self._frame_layout.setSpacing(0)
        self._frame_layout.setContentsMargins(15,10,15,10)
        self._frame_layout.setAlignment(QtCore.Qt.AlignTop)

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

        self._frame_layout.addWidget(self._ramp_display)
        self._frame_layout.addWidget(SeparatorWidgetClass.SeparatorHWidget())
        self._frame_layout.addWidget(self._collapsible_folder)

        self._base_frame.setLayout(self._frame_layout)
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)

        self._layout.addWidget(self._widget_buttons)
        self._layout.addWidget(self._base_frame)
        self.setLayout(self._layout)

        self._init_done = True

    def mapRange_Clamp(self,value, inRangeA, inRangeB, outRangeA, outRangeB):
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
        return self._ramp_display.ramp().scene

    def updateSlider_width(self,*args):
        self._slider.updateWidth(args[0])

    def newHandle(self, position, control):
        return self._slider.newHandle(position, control)

    def newControl(self,index, pos, value, interp):
        if self._placeholder:
            self._stack.removeWidget(self._placeholder)
            self._placeholder = None

        new_control = RampControlsWidget(self)
        new_control.setPosValue(pos)
        new_control.setValue(value)
        new_control.setInterp(interp)

        self._stack.insertWidget(index, new_control)
        self._stack.setCurrentWidget(new_control)

        for i in range(0,self._stack.count()):
            self._stack.widget(i).setMaxNum(self._stack.count())
            self._stack.widget(i).setNum(i+1)

        return new_control


    def get_ramp(self):
        return self.graphicScene().get_ramp_values()

    def setRamp(self,positions,values,interps):
        graph_scene_y_min = self._ramp_display.ramp().scene.min_height_pos()
        graph_scene_y_max = self._ramp_display.ramp().scene.max_height_pos()

        for x in enumerate(positions):
            x_pos = self.mapRange_Clamp(x[1], 0, 1, -152.0, self._ramp_display.ramp().width - 155)
            y_pos = self.mapRange_Clamp(values[x[0]], 0, 1, graph_scene_y_min, graph_scene_y_max)
            self._ramp_display.ramp().scene.addRampPoint(x_pos,y_pos, interps[x[0]])


class RampWidgetButtons(QtWidgets.QWidget):

    def __init__(self,parent):
        super(RampWidgetButtons, self).__init__()
        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setSpacing(5)
        self._layout.setContentsMargins(0,10,0,0)
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
        self._rev_domain.setFixedSize(20,20)
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
            'Constant' : self.constantSetup,
            'Hill' : self.hillSetup,
            'Linear' : self.linearSetup,
            'Round' : self.roundSetup,
            'Sharp' : self.sharpSetup,
            'Smooth' : self.smoothSetup,
            'Steps' : self.stepsSetup,
            'Valley' : self.valleySetup
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
        self._parent.sliderWidget().clearHandles()
        self._parent.graphicScene().clearPoints()
        self._parent.itemData().clear_groups()
        for i in range(0,self._parent.widgetStack().count()):
            self._parent.widgetStack().removeWidget(self._parent.widgetStack().widget(i))
        self._parent.setRamp(*func())


    def update_chart(self,state):
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
        return [0,0.5,1], [0,1,0], [5,5,5]

    def linearSetup(self):
        return [0,1], [0,1], [1,1]

    def roundSetup(self):
        return [0,0.8,1], [0,0,1], [4,4,4]

    def sharpSetup(self):
        return [0,0,1], [0,1,1], [4,4,4]

    def smoothSetup(self):
        return [0,1], [0,1], [3,3]

    def stepsSetup(self):
        return [0,0.25, 0.5, 0.75], [0, 0.33, 0.66, 1], [0,0,0,0]

    def valleySetup(self):
        return [0,0.5,1], [1,0,1], [3,3,3]

    def testSetup(self):
        return [0,0.5,1], [0,1,0.2],[6,6,6]



class RampWidgetData:

    def __init__(self):
        super(RampWidgetData, self).__init__()
        self._groupItemA: Dict[Any,List[Any]] = {}
        self._groupItemB: Dict[Any,List[Any]] = {}
        self._groupItemC: Dict[Any, List[Any]] = {}


    def addGroup(self,sceneItem, handle_index, controls) -> None:
        listA = [handle_index, controls]
        self._groupItemA[sceneItem] = listA

        listB = [sceneItem,controls]
        self._groupItemB[handle_index] = listB

        listC = [sceneItem,handle_index]
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

        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Slider))
        self.move(0,40)
        self.setFixedWidth(398)

    def baseParent(self,parent):
        self._base_parent = parent


    def handlePosition(self,index):
        return self.slider_positions[index]

    def sort_dict_handles(self):
        self._slider_pos_cont = dict(sorted(self._slider_pos_cont.items(), key=lambda item: item[1]))


    def newHandle(self,position, control):
        self.slider_positions.append(position)
        self._slider_pos_cont[control] = position
        self.sort_dict_handles()
        self.update()
        return len(self.slider_positions) - 1

    def removeHandle(self,index, control):
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
        self.setFixedWidth(width+10)


    def update_height(self, height):
        self.move(0, height)


    def keyPressEvent(self, event) -> None:
        if event.key() == QtCore.Qt.Key_Backspace or event.key() == QtCore.Qt.Key_Delete:
            itemlist = self._base_parent.itemData().getGroupB()[self.currentIndex]
            self._base_parent.itemData().removeGroupItems(itemlist[1])
            self._base_parent.graphicScene().removePoint(itemlist[0])
            self.removeHandle(self.currentIndex,self._other_parent)
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
            self._current_handle = self.style().hitTestComplexControl(QtWidgets.QStyle.CC_Slider, self.opt, event.pos(), self)

            if math.isclose(pos, i[1],abs_tol=25000):
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


    def moveSlider(self,index,control, pos):
        self.slider_positions[index] = pos
        self._slider_pos_cont[control] = pos
        self.update()




class PointNumWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(PointNumWidget,self).__init__()
        self._parent = parent
        self._other_parent = None
        self._base_index = 0

        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0,5,0,5)
        self._layout.setAlignment(QtCore.Qt.AlignLeft)

        self._index_widget = LineEditWidgets.LineEditIntWidgetClass(no_num_button=False)
        self._index_widget.baseWidget().setToolTip('Mouse wheel to change Selection.')
        self._index_widget.baseWidget().setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")


        self._add_button = QtWidgets.QPushButton('+')
        self._add_button.setFont(QtGui.QFont('+',8,QtGui.QFont.Bold))
        self._add_button.setFixedWidth(25)
        self._add_button.setProperty('class', 'add_button')

        self._sub_button = QtWidgets.QPushButton('-')
        self._sub_button.setFont(QtGui.QFont('-', 12, QtGui.QFont.Bold))
        self._sub_button.setFixedWidth(25)
        self._sub_button.setProperty('class','sub_button')

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
        self._index_widget.baseWidget().valueChanged.connect(self.updateSelection)

    def controllerParent(self):
        return self._other_parent

    def setControllerParent(self, parent):
        self._other_parent = parent

    def setBase(self, value):
        self._base_index = value
        self._index_widget.setValue(value)

    def setRange(self,maxValue):
        self._index_widget.setRange(1,maxValue)


    def updateSelection(self, value):
        if self._index_widget.wheelState():
            controls = list(self._parent.slider_widget().handle_dict_positions().keys())
            self._parent.widgetStack().setCurrentWidget(controls[value - 1])
            itemlist = self._parent.itemData().getGroupC()[controls[value - 1]]
            itemlist[0].parentScene().itemSelect(itemlist[0])
            self._index_widget.setValue(self._base_index)
            self.setFocus()



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
        super(RampControlsWidget,self).__init__()
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


    def withLabel(self,text, widget_obj):
        hor_layout = QtWidgets.QHBoxLayout()
        hor_layout.setSpacing(5)
        hor_layout.setContentsMargins(0,0,0,0)
        
        hor_layout.addWidget(QtWidgets.QLabel(text = text))
        hor_layout.addWidget(widget_obj)
        
        self._layout.addLayout(hor_layout)


    def updatePath(self,index):
        itemlist = self._parent.itemData().getGroupC()[self]
        self._parent.graphicScene().updateInterp(itemlist[0], index)
        self._parent.graphicScene().drawPath()


    def changeSelection(self, value):
        if self._notSelf:
            self._parent.widgetStack().setCurrentIndex(value-1)
            other = self._parent.widgetStack().currentWidget()
            itemlist = self._parent.itemData().getGroupC()[other]
            itemlist[0].parentScene().itemSelect(itemlist[0])
            self.setNum(self._base_num)



    def updatePosition(self, value):
        if self._parent.bInit():
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

    def setMaxNum(self,max_num: int):
        self._num_widget.setRange(max_num)

    def setPosValue(self, position: float):
        self._pos_slider.setValue(position)

    def setValue(self, value: float):
        self._val_slider.setValue(value)

    def setInterp(self, index: int):
        self._menu_interp.setItem(index)


        

class RampGraphicDisplayOuter(QtWidgets.QWidget):

    def __init__(self,parent):
        super(RampGraphicDisplayOuter, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(5,0,5,10)
        self._display_height = 50

        self._parent = parent
        self.setFixedHeight(self._display_height + 15)

        self._ramp_display = RampGraphicViewer(parent)

        self._layout.addWidget(self._ramp_display)
        self.setLayout(self._layout)

    def ramp(self):
        return self._ramp_display

    def set_height(self, height):
        self._display_height = height + 15
        self._ramp_display.set_view_height(height)
        self.setFixedHeight(self._display_height)


class RampGraphicViewer(QtWidgets.QGraphicsView):

    def __init__(self,parent):
        super(RampGraphicViewer, self).__init__(parent)
        self.scene = RampGraphicScene(parent)
        self.scene.setSceneRect(0, 0, self.size().width(), self.size().height())
        self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(45,45,45)))
        self.setScene(self.scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self._view_height = 50

        self.setFixedHeight(self._view_height)
        self._parent = parent

        self.width = 388


    def resizeEvent(self, event) -> None:
        self.width = self.size().width()
        self._parent.updateSlider_width(self.size().width())
        self.scene.sizeChange(self.width)


    def set_view_height(self, height):
        self._view_height = height
        self.setFixedHeight(self._view_height)



class RampGraphicScene(QtWidgets.QGraphicsScene):

    def __init__(self, parent):
        super(RampGraphicScene, self).__init__()
        self._parent = parent

        self.width = 376
        self._min = -152 # 148 old
        self._sub = 155 # 145 old

        self._y_min = 30.0 # 105.0 old
        self._y_max = -18.0 # -93.0 old

        self.__doOnce = True
        self._show_grid = False

        self.points = []
        self.interps = {}

        self.xLines = []
        self.yLines = []
        self.xText = []
        self.yText = []

        self.scenePath = None
        self.lastPoint = None
        self.currentPoint = None
        self._mouseState = False

        self.updateGridY()

    def keyPressEvent(self, event) -> None:
        if event.key() == QtCore.Qt.Key_Backspace or event.key() == QtCore.Qt.Key_Delete:
            itemlist = self._parent.itemData().getGroupA()[self.currentPoint]
            self._parent.itemData().removeGroupItems(itemlist[1])
            self.removePoint(self.currentPoint)
            self._parent.slider_widget().removeHandle(itemlist[0],itemlist[1])
            self._parent.widgetStack().removeWidget(itemlist[1])
            itemlist[1].deleteLater()

            for index, i in enumerate(list(self._parent.slider_widget().handle_dict_positions().keys())):
                i.setNum(index + 1)

    def min_height_pos(self):
        return self._y_min

    def max_height_pos(self):
        return self._y_max

    def scene_collapsed(self):
        self._y_min = 180 if self._show_grid else 30.0

        for p in self.points:
            newPos = self._parent.mapRange_Clamp(p.pos().y(), 30.0 if self._show_grid else 180.0, self._y_max, self._y_min, self._y_max)
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
            new_x_pos = self._parent.mapRange_Clamp(p.pos().x(), self._min, self.width - self._sub, self.width - self._sub, self._min)
            p.setPos(new_x_pos, p.pos().y())
            self.sortPoints()
            self.updateValues(p)

        for index, sort_p in enumerate(self.points):
            data_item = self._parent.itemData().getGroupA()[sort_p]
            data_item[1].setNum(index + 1)


        # self._parent.widgetStack()
        #
        # for i in range(0,self._parent.widgetStack().count()):
        #     self._parent.widgetStack().widget(i).setMaxNum(self._parent.widgetStack().count())
        #     self._parent.widgetStack().widget(i).setNum(i+1)

    def complement_points(self):
        for p in self.points:
            new_y_pos = self._parent.mapRange_Clamp(p.pos().y(), self._y_min, self._y_max, self._y_max, self._y_min)
            p.setPos(p.pos().x(), new_y_pos)
            self.updateValues(p)


    def sizeChange(self, width):
        self.width = width
        self.updateGridX()
        if self.__doOnce:
            self.__doOnce = False
            if len(self.points) <= 0:
                self._parent.setRamp(*self._parent.actionButtons().linearSetup())
        else:
            self.updatePoints()
            self.drawPath()


    def mousePressEvent(self, event) -> None:
        pos = event.scenePos()
        item = self.itemAt(pos, QtGui.QTransform())

        if isinstance(item, EllipseItem):
            if self.selectedItems()[0] != item:
                self.itemSelect(item)
                itemlist = self._parent.itemData().getGroupA()[item]
                self._parent.widgetStack().setCurrentWidget(itemlist[1])
                return
            else:
                self._mouseState = True
                QtWidgets.QGraphicsScene.mousePressEvent(self, event)
                return
        else:
            pos.setX(pos.x() - 8)
            pos.setY(pos.y() - 8)
            self.addNew_EllipsePoint(pos,self.interps[self.lastPoint])
            return

    def mouseMoveEvent(self, event) -> None:
        pos_y = self.selectedItems()[0].pos().y()
        pos_x = self.selectedItems()[0].pos().x()
        if pos_y > self._y_max and pos_y < self._y_min:
            super(RampGraphicScene, self).mouseMoveEvent(event)

            if self._mouseState:
                self.updateValues(self.selectedItems()[0])



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
            for i in range(0,19):
                num += 0.05
                x_text.append(str(round(num, 3)))

        elif self.width >= 1500:
            num = 0
            x_text = []
            for i in range(0,49):
                num += 0.02
                x_text.append(str(round(num,3)))
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
            for i in range(0,len(self.xLines)):
                self.removeItem(self.xLines[i])
                self.removeItem(self.xText[i])

            self.xLines.clear()
            self.xText.clear()

        for i in range(0, len(x_text)):
            text_item = self.addText(x_text[i], QtGui.QFont(x_text[i], 8, QtGui.QFont.Normal))
            text_item.setDefaultTextColor(text_color)
            text_item.setPos(xpos-4, bottom)

            new_line = self.addLine(xpos + 10, -100, xpos + 10, bottom, line_pen)
            self.xLines.append(new_line)
            self.xText.append(text_item)

            new_line.setVisible(self._show_grid)
            text_item.setVisible(self._show_grid)

            xpos += (self.width-4) / divLen


    def updateGridY(self):
        line_pen = QtGui.QPen(QtGui.QColor(80, 80, 80), 1, QtCore.Qt.SolidLine)
        text_color = QtGui.QColor(80, 80, 80)

        ypos = 140 #64 old
        y_text = ['0.2', '0.4', '0.6', '0.8']

        for i in range(0,len(y_text)):
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
        item.setBrush(QtGui.QColor(0,205,255))

        if self.lastPoint is not None:
            self.lastPoint.setBrush(QtGui.QColor(0,0,0))
            self.lastPoint.setSelected(False)

        self.currentPoint = item
        self.lastPoint = item


    def removePoint(self,item):
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
        next_point = self.points[index+1] if index < (len(self.points)-1) else self.points[index-1]
        x_pos = (point.pos().x() + next_point.pos().x()) / 2
        y_pos = (point.pos().y() + next_point.pos().y()) / 2
        interp = self.interps[point]
        position = QtCore.QPointF(x_pos, y_pos)
        self.addNew_EllipsePoint(position, interp)


    def get_ramp_values(self):
        points_pos = []
        points_value = []
        for p in self.points:
            points_pos.append(self._parent.mapRange_Clamp(p.pos().x(), self._min, self.width - self._sub, 0, 1))
            points_value.append(self._parent.mapRange_Clamp(p.pos().y(), self._y_min, self._y_max, 0, 1))

        return { 'positions':points_pos, 'values': points_value, 'interpolations': list(self.interps.values()) }


    def addRampPoint(self,pos,value, interp):
        position = QtCore.QPointF(pos, value)
        self.addNew_EllipsePoint(position,interp)


    def addNew_EllipsePoint(self, position,interp=0):
        self._parent.setbInit(False)

        newEllipse = EllipseItem(5,5,8,8)
        newEllipse.setParent(self)
        newEllipse.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 2, QtCore.Qt.SolidLine))
        newEllipse.setBrush(QtGui.QBrush(QtGui.QColor(0, 205, 255)))
        newEllipse.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable | QtWidgets.QGraphicsItem.ItemIsSelectable)
        newEllipse.setPos(position)
        newEllipse.setSelected(True)
        newEllipse.setZValue(1)
        self.addItem(newEllipse)
        self.points.append(newEllipse)
        self.sortPoints()
        self.interps[newEllipse] = interp

        slider_pos = self._parent.mapRange_Clamp(position.x(),self._min,self.width - self._sub, 0, 1000000.0)
        control_x_pos = self._parent.mapRange_Clamp(position.x(),self._min, self.width - self._sub, 0, 1)
        control_y_pos = self._parent.mapRange_Clamp(position.y(), self._y_min, self._y_max, 0, 1)

        control_widget = self._parent.newControl(self.points.index(newEllipse),control_x_pos, control_y_pos, interp)
        slider_index = self._parent.newHandle(int(slider_pos), control_widget)
        self._parent.itemData().addGroup(newEllipse, slider_index, control_widget)

        self.itemSelect(newEllipse)
        self.drawPath()
        self._parent.setbInit(True)


    def sortPoints(self):
        positions = []
        for i in self.points:
            positions.append(i.pos().x())

        pos_sorted = sorted(positions)
        points_sorted = []
        for i in range(0,len(pos_sorted)):
            current_point_pos = self.points[i].pos().x()
            index = pos_sorted.index(current_point_pos)
            points_sorted.insert(index, self.points[i])

        self.points = points_sorted



    def updatePoints(self):
        for i in self.points:
            itemlist = self._parent.itemData().getGroupA()[i]
            pos = self._parent.slider_widget().handlePosition(itemlist[0])
            newPos = self._parent.mapRange_Clamp(pos,0 , 1000000.0, self._min, self.width - self._sub)
            i.setPos(newPos, i.pos().y())


    def updateInterp(self,item,index):
        self.interps[item] = index

    def updateValues(self, item):
        itemlist = self._parent.itemData().getGroupA()[item]

        slider_pos = self._parent.mapRange_Clamp(item.pos().x(), self._min, self.width - self._sub, 0, 1000000.0)
        self._parent.slider_widget().moveSlider(itemlist[0],itemlist[1], slider_pos)

        control_x_pos = self._parent.mapRange_Clamp(item.pos().x(),self._min, self.width - self._sub, 0, 1)
        control_y_pos = self._parent.mapRange_Clamp(item.pos().y(), self._y_min, self._y_max, 0, 1)

        itemlist[1].setPosValue(control_x_pos)
        itemlist[1].setValue(control_y_pos)

        self._parent.slider_widget().sort_dict_handles()
        self.sortPoints()

        for index, i in enumerate(list(self._parent.slider_widget().handle_dict_positions().keys())):
            i.setNum(index + 1)

        self.drawPath()


    def moveXItem(self, item, pos_x):
        pos_x = self._parent.mapRange_Clamp(pos_x, 0, 1000000.0, self._min, self.width - self._sub)
        item.setPos(pos_x, item.pos().y())
        self.sortPoints()

    def moveYItem(self, item, pos_y):
        pos_y = self._parent.mapRange_Clamp(pos_y, 0, 1000000.0, self._y_min, self._y_max)
        item.setPos(item.pos().x(), pos_y)


    def drawPath(self):
        addition = 10
        path = QtGui.QPainterPath()
        path.moveTo(-160,250)
        path.lineTo(-160, self.points[0].pos().y() + addition)

        if len(self.points) != 1:
            for i, p in enumerate(self.points): #Constant
                if self.interps[p] == 0:
                    path.lineTo(p.pos().x() + addition, p.pos().y() + addition)
                    if p != self.points[-1]:
                        path.lineTo(self.points[i + 1].pos().x() + addition, p.pos().y() + addition)

                elif self.interps[p] == 1: #Linear
                    path.lineTo(p.pos().x() + addition, p.pos().y() + addition)

                elif self.interps[p] == 2: #Catmull-Rom
                    print('Catmull-Rom Interpolation has not yet been implemented. Sorry!!!')
                    # pts = []
                    # for ip in self.points:
                    #     if self.interps[p] == 2:
                    #         pos = ip.pos().x() + addition,ip.pos().y() + addition
                    #         pts.append(list(pos))
                    #
                    # extra_start_pt = (pts[0][0] - 10 , pts[0][1])
                    # extra_end_pt = (pts[-1][0] + 10, pts[-1][1])
                    # pts.insert(0,list(extra_start_pt))
                    # pts.insert(len(pts), list(extra_end_pt))
                    #
                    # c = CatmullRomChain(pts)
                    # xpos, ypos = zip(*c)
                    # for i, x in enumerate(xpos):
                    #     path.lineTo(x, ypos[i])
                    #
                    # break
                elif self.interps[p] == 3: #Monotone Cubic
                    print('Monotone Cubic Interpolation has not yet been implemented. Sorry!!!')
                    # if len(self.points) >= 3:
                    #     pts_x = []
                    #     pts_y = []
                    #     for ip in self.points:
                    #         if self.interps[p] == 3:
                    #             pts_x.append(ip.pos().x() + addition)
                    #             pts_y.append(ip.pos().y() + addition)
                    #
                    #     extra_start_x = pts_x[0] - 10
                    #     extra_start_y = pts_y[0]
                    #     extra_end_x = pts_x[-1] + 10
                    #     extra_end_y = pts_y[-1]
                    #
                    #     pts_x.insert(0,extra_start_x)
                    #     pts_y.insert(0,extra_start_y)
                    #     pts_x.insert(len(pts_x),extra_end_x)
                    #     pts_y.insert(len(pts_y), extra_end_y)
                    #
                    #     intrp = monospline(pts_x, pts_y)
                    #     x_intrp = np.linspace(min(pts_x), max(pts_x), 100)
                    #     y_intrp = intrp.evaluate(x_intrp)
                    #
                    #     for i, x in enumerate(x_intrp):
                    #         path.lineTo(x, y_intrp[i])
                    #
                    #     break

                elif self.interps[p] == 4: #Bezier
                    pts = []
                    for ip in self.points:
                        if self.interps[p] == 4:
                            pos = ip.pos().x() + addition, ip.pos().y() + addition
                            pts.append(pos)

                    for point in bezier_curve_range(100, pts):
                        path.lineTo(point[0], point[1])

                    break

                elif self.interps[p] == 5: #B-Spline
                    print('B-Spline Interpolation has not yet been implemented. Sorry!!!')
                    # if len(self.points) >= 3:
                    #     pts = []
                    #     for ip in self.points:
                    #         if self.interps[p] == 5:
                    #             pos = ip.pos().x() + addition, ip.pos().y() + addition
                    #             pts.append(pos)
                    #
                    #     # extra_start_pt = (pts[0][0] - 10, pts[0][1])
                    #     # extra_end_pt = (pts[-1][0], pts[-1][1] + 10)
                    #     # pts.insert(0, extra_start_pt)
                    #     # pts.insert(len(pts), extra_end_pt)
                    #
                    #     cv = np.array(pts)
                    #     spline = bspline(cv)
                    #
                    #     for i in range(0,len(spline)):
                    #         path.lineTo(spline[i][0],spline[i][1])
                    #
                    #     break

                elif self.interps[p] == 6: #Hermit
                    print('Hermite Interpolation has not yet been implemented. Sorry!!!')


        distance = (self.width - self._sub) - self.points[-1].pos().x()
        path.lineTo(self.points[-1].pos().x() + abs(distance) + 30, self.points[-1].pos().y() + addition)
        path.lineTo(self.points[-1].pos().x() + abs(distance) + 30, 250.0)

        if self.scenePath:
            self.removeItem(self.scenePath)

        self.scenePath = self.addPath(path,QtGui.QPen(QtGui.QColor(25, 25, 25, 125), 3, QtCore.Qt.SolidLine), QtGui.QBrush(QtGui.QColor(200, 200, 200,125)))



class EllipseItem(QtWidgets.QGraphicsEllipseItem):
    def paint(self, painter, option, widget):
        option.state &= ~QtWidgets.QStyle.State_Selected
        super(EllipseItem, self).paint(painter, option, widget)


    def setParent(self, parent):
        self._parent = parent

    def parentScene(self):
        return self._parent






def CatmullRomSpline(P0, P1, P2, P3, nPoints=100):
    """
    P0, P1, P2, and P3 should be (x,y) point pairs that define the Catmull-Rom spline.
    nPoints is the number of points to include in this curve segment.
    """
    # Convert the points to numpy so that we can do array multiplication
    # P0, P1, P2, P3 = map(np.array, [P0, P1, P2, P3])
    P0, P1, P2, P3 = list(P0), list(P1), list(P2), list(P3)

    # Parametric constant: 0.5 for the centripetal spline, 0.0 for the uniform spline, 1.0 for the chordal spline.
    alpha = 1.0
    # Premultiplied power constant for the following tj() function.
    alpha = alpha/2

    def tj(ti, Pi, Pj):
        xi, yi = Pi
        xj, yj = Pj
        return ((xj-xi)**2 + (yj-yi)**2)**alpha + ti

    def linspace(start, stop, n):
        if n == 1:
            yield stop
            return
        h = (stop - start) / (n - 1)
        for i in range(n):
            yield start + h * i

    def reshape(lst, shape):
        if len(shape) == 1:
            return lst
        n = reduce(mul, shape[1:])
        return [reshape(lst[i * n:(i + 1) * n], shape[1:]) for i in range(len(lst) // n)]

    # Calculate t0 to t4
    t0 = 0
    t1 = tj(t0, P0, P1)
    t2 = tj(t1, P1, P2)
    t3 = tj(t2, P2, P3)

    # Only calculate points between P1 and P2
    # t = np.linspace(t1, t2, nPoints)

    a = list(linspace(t1, t2, nPoints))
    t = [ round(x,8) for x in a ]
    # t = []
    # for x in a:
    #     i = [x]; t.append(i)


    # Reshape so that we can multiply by the points P0 to P3
    # and get a point for each value of t.
    # t = t.reshape(len(t), 1)
    t = reshape(t, [1])
    print(t)
    A1 = (t1-t)/(t1-t0)*P0 + (t-t0)/(t1-t0)*P1
    A2 = (t2-t)/(t2-t1)*P1 + (t-t1)/(t2-t1)*P2
    A3 = (t3-t)/(t3-t2)*P2 + (t-t2)/(t3-t2)*P3

    B1 = (t2-t)/(t2-t0)*A1 + (t-t0)/(t2-t0)*A2
    B2 = (t3-t)/(t3-t1)*A2 + (t-t1)/(t3-t1)*A3

    C = (t2-t)/(t2-t1)*B1 + (t-t1)/(t2-t1)*B2
    return C



def CatmullRomChain(P):
    """
    Calculate Catmull-Rom for a chain of points and return the combined curve.
    """
    sz = len(P)

    # The curve C will contain an array of (x, y) points.
    C = []
    for i in range(sz-3):
        c = CatmullRomSpline(P[i], P[i+1], P[i+2], P[i+3])
        C.extend(c)

    return C





#------------------------------------------------------------------------------------------------

# class monospline:
#     def __init__(self, x, y):
#         self.x = np.array(x)
#         self.y = np.array(y)
#         self.n = self.y.size
#         self.h = self.x[1:] - self.x[:-1]
#         self.m = (self.y[1:] - self.y[:-1]) / self.h
#         self.a = self.y[:]
#         self.b = self.compute_b(self.x, self.y)
#         self.c = (3 * self.m - self.b[1:] - 2 * self.b[:-1]) / self.h
#         self.d = (self.b[1:] + self.b[:-1] - 2 * self.m) / (self.h * self.h)
#
#     def compute_b(self, t, r):
#         b = np.empty(self.n)
#         for i in range(1, self.n - 1):
#             is_mono = self.m[i - 1] * self.m[i] > 0
#             if is_mono:
#                 b[i] = 3 * self.m[i - 1] * self.m[i] / (max(self.m[i - 1], self.m[i]) + 2 * min(self.m[i - 1], self.m[i]))
#             else:
#                 b[i] = 0
#             if is_mono and self.m[i] > 0:
#                 b[i] = min(max(0, b[i]), 3 * min(self.m[i - 1], self.m[i]))
#             elif is_mono and self.m[i] < 0:
#                 b[i] = max(min(0, b[i]), 3 * max(self.m[i - 1], self.m[i]))
#
#         b[0] = ((2 * self.h[0] + self.h[1]) * self.m[0] - self.h[0] * self.m[1]) / (self.h[0] + self.h[1])
#         b[self.n - 1] = ((2 * self.h[self.n - 2] + self.h[self.n - 3]) * self.m[self.n - 2]
#                          - self.h[self.n - 2] * self.m[self.n - 3]) / (self.h[self.n - 2] + self.h[self.n - 3])
#         return b
#
#     def evaluate(self, t_intrp):
#         ans = []
#         for tau in t_intrp:
#             i = np.where(tau >= self.x)[0]
#             if i.size == 0:
#                 i = 0
#             else:
#                 i = i[-1]
#             i = min(i, self.n-2)
#             res = self.a[i] + self.b[i] * (tau - self.x[i]) + self.c[i] * np.power(tau - self.x[i], 2.0) + self.d[i] * np.power(tau - self.x[i], 3.0) #original curve r(t)
#             ans.append(res)
#         return ans
#
#     def evaluate_derivative(self, t_intrp):
#         ans = []
#         if not hasattr(t_intrp, "__len__"):
#             t_intrp = np.array([t_intrp])
#         for tau in t_intrp:
#             i = np.where(tau >= self.x)[0]
#             if i.size == 0:
#                 i = 0
#             else:
#                 i = i[-1]
#             i = min(i, self.n-2)
#             res = self.b[i] + 2 * self.c[i] * (tau - self.x[i]) + 3 * self.d[i] * np.power(tau - self.x[i], 2.0)
#             ans.append(res)
#         if len(ans) == 1:
#             return ans[0]
#         else:
#             return ans
#
#     def evaluate_forward(self, t_intrp):
#         ans = []
#         for tau in t_intrp:
#             i = np.where(tau >= self.x)[0]
#             if i.size == 0:
#                 i = 0
#             else:
#                 i = i[-1]
#             i = min(i, self.n-2)
#             res = self.a[i] + self.b[i] * (2 * tau - self.x[i]) + self.c[i] * (tau - self.x[i]) * (3*tau - self.x[i]) \
#                   + self.d[i] * np.power(tau - self.x[i], 2.0) * (4 * tau - self.x[i]) # d(xy)/dx
#             ans.append(res)
#         return ans



#------------------------------------------------------------------------------------------------
# Bezier

def binomial(i, n):
    """Binomial coefficient"""
    return math.factorial(n) / float(
        math.factorial(i) * math.factorial(n - i))


def bernstein(t, i, n):
    """Bernstein polynom"""
    return binomial(i, n) * (t ** i) * ((1 - t) ** (n - i))


def bezier(t, points):
    """Calculate coordinate of a point in the bezier curve"""
    n = len(points) - 1
    x = y = 0
    for i, pos in enumerate(points):
        bern = bernstein(t, i, n)
        x += pos[0] * bern
        y += pos[1] * bern
    return x, y


def bezier_curve_range(n, points):
    """Range of points in a curve bezier"""
    for i in range(n):
        t = i / float(n - 1)
        yield bezier(t, points)





# def bspline(cv, n=100, degree=3, periodic=False):
#     """ Calculate n samples on a bspline
#
#         cv :      Array ov control vertices
#         n  :      Number of samples to return
#         degree:   Curve degree
#         periodic: True - Curve is closed
#                   False - Curve is open
#     """
#
#     # If periodic, extend the point array by count+degree+1
#     cv = np.asarray(cv)
#     count = len(cv)
#
#     if periodic:
#         factor, fraction = divmod(count + degree + 1, count)
#         cv = np.concatenate((cv,) * factor + (cv[:fraction],))
#         count = len(cv)
#         degree = np.clip(degree, 1, degree)
#
#     # If opened, prevent degree from exceeding count-1
#     else:
#         degree = np.clip(degree, 1, count - 1)
#
#     # Calculate knot vector
#     kv = None
#     if periodic:
#         kv = np.arange(0 - degree, count + degree + degree - 1, dtype='int')
#     else:
#         kv = np.concatenate(([0] * degree, np.arange(count - degree + 1), [count - degree] * degree))
#
#     # Calculate query range
#     u = np.linspace(periodic, (count - degree), n)
#
#     # Calculate result
#     return np.array(si.splev(u, (kv, cv.T, degree))).T



#------------------------------------------------------------------------------------------------------
