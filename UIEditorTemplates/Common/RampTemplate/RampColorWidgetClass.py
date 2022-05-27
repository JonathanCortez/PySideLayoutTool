import math
from operator import add, sub
from PySide2 import QtWidgets, QtCore, QtGui

from PySideLayoutTool.UIEditorTemplates.Folder.CollapisbleFolderTemplate import CollapisbleFolderWidgetClass
from PySideLayoutTool.UIEditorTemplates.Common.SliderTemplate import SliderWidgetClass
from PySideLayoutTool.UIEditorTemplates.Common.SeparatorTemplate import SeparatorWidgetClass
from PySideLayoutTool.UIEditorTemplates.Common.LineEditTemplate import LineEditWidgets
from PySideLayoutTool.UIEditorTemplates.Common.ComboBoxTemplate import ComboBoxWidgetClass

from PySideLayoutTool.UIEditorLib import UIEditorIconFactory
from typing import Dict, List, Any

from ..ColorTemplate import ColorWidgetClass


class RampColorWidgetSetup(QtWidgets.QWidget):

    def __init__(self,parent):
        super(RampColorWidgetSetup, self).__init__(parent)
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0,0,0,0)
        self._parent = parent

        self._init_done = False
        self._new_control_widget = None

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
        self._placeholder.setFixedHeight(160)
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

    def color_rect_scene(self):
        return self._ramp_display.color_rect()

    def updateSlider_width(self,*args):
        self._slider.updateWidth(args[0])

    def newHandle(self, position, control):
        return self._slider.newHandle(position, control)


    def _new_control(self,index, pos, color, interp):
        if self._placeholder:
            self._stack.removeWidget(self._placeholder)
            self._placeholder = None

        self._new_control_widget.setPosValue(pos)
        self._new_control_widget.set_rgb(color)
        self._new_control_widget.setInterp(interp)

        self._stack.insertWidget(index, self._new_control_widget)
        self._stack.setCurrentWidget(self._new_control_widget)

        for i in range(0,self._stack.count()):
            self._stack.widget(i).setMaxNum(self._stack.count())
            self._stack.widget(i).setNum(i+1)

    def get_ramp(self):
        return self.graphicScene().get_ramp_values()


    def color_ramp_setup(self,index, pos, color, interp):
        self._new_control_widget = RampControlsWidget(self)
        self._new_control_widget.set_block(True)
        slider_pos = self.mapRange_Clamp(pos, 0, 1, 0, 1000000)
        slider_index = self.newHandle(int(slider_pos), self._new_control_widget)

        color_obj = QtGui.QColor()
        color_obj.setRgbF(color[0], color[1], color[2])

        self.itemData().addGroup(index, slider_index, self._new_control_widget)
        self._new_control(index, pos, color, interp)
        self._new_control_widget.set_block(False)

        return color_obj

    def setRamp(self,positions, colors, interps):
        color_range = []
        color_at_range = []

        for index, pos in enumerate(positions):
            color_range.append(self.color_ramp_setup(index, pos, colors[index], interps[index]))
            color_at_range.append(float(pos))

        self.color_rect_scene().set_color_rect_values(color_range, color_at_range)
        self.color_rect_scene().update_color_rect()


class RampWidgetData:

    def __init__(self):
        super(RampWidgetData, self).__init__()
        self._groupItemA: Dict[Any,List[Any]] = {}
        self._groupItemB: Dict[Any,List[Any]] = {}
        self._groupItemC: Dict[Any, List[Any]] = {}


    def addGroup(self,color_index, handle_index, control) -> None:
        listA = [handle_index, control]
        self._groupItemA[color_index] = listA

        listB = [color_index, control]
        self._groupItemB[handle_index] = listB

        listC = [color_index, handle_index]
        self._groupItemC[control] = listC

    def update_indexs(self,new_index, operator_type):
        for i in self._groupItemA:
            if self._groupItemA[i][0] == new_index:
                self._groupItemA[i][0] = operator_type(new_index, 1)

            if i == new_index:
                self._groupItemA[operator_type(new_index,1)] = self._groupItemA[i]
                del self._groupItemA[i]


        for i in self._groupItemB:
            if self._groupItemB[i][0] == new_index:
                self._groupItemB[i][0] = operator_type(new_index,1)

            if i == new_index:
                self._groupItemB[operator_type(new_index,1)] = self._groupItemB[i]
                del self._groupItemB[i]


        for i in self._groupItemC:
            if self._groupItemC[i][0] == new_index:
                self._groupItemC[i][0] = operator_type(new_index,1)
                self._groupItemC[i][1] = operator_type(new_index, 1)

    def update_handle_index(self,old_index, new_index):
        pass

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
        self.__menu.addAction('Black Body')
        self.__menu.addAction('Grayscale')
        self.__menu.addAction('Infra-Red')
        self.__menu.addAction('Two-Tone')
        self.__menu.addAction('White to Red')
        self._preset_menu.setMenu(self.__menu)

        self._type_action = {
            'Black Body' : self.black_body_setup,
            'Grayscale' : self.grayscale_setup,
            'Infra-Red' : self.infra_red_setup,
            'Two-Tone' : self.two_tone_setup,
            'White to Red' : self.white_to_red_setup
        }

        self.__menu.triggered.connect(self.updateRamp)

        self._layout.addWidget(self._label)
        self._layout.addWidget(self._spacing_item)
        self._layout.addWidget(self._rev_domain)
        self._layout.addWidget(self._comp_ramp)
        self._layout.addWidget(self._preset_menu)

        self.setLayout(self._layout)



    def setLabel(self, text: str):
        self._label.setText(text)

    def updateRamp(self, action):
        func = self._type_action[action.text()]
        self._parent.slider_widget().clearHandles()
        self._parent.color_rect_scene().clear_colors()
        self._parent.itemData().clear_groups()
        for i in range(0,self._parent.widgetStack().count()):
            self._parent.widgetStack().removeWidget(self._parent.widgetStack().widget(i))
        self._parent.setRamp(*func())


    def reverse_chart(self):
        colors = [c.getRgbF() for c in self._parent.color_rect_scene().get_colors()]

        for index, key in enumerate(self._parent.slider_widget().handle_dict_positions()):
            value = self._parent.slider_widget().handle_dict_positions()[key]
            new_value = self._parent.mapRange_Clamp(value, 0, 1000000, 0, 1)
            itemlist = self._parent.itemData().getGroupC()[key]
            self._parent.slider_widget().moveSlider(itemlist[1],self._parent.mapRange_Clamp(1 - new_value, 0, 1, 0, 1000000), key)
            key.setPosValue(1 - new_value)
            key.setValue(colors[index])

        self._parent.slider_widget().sort_dict_handles()

        for index, i in enumerate(list(self._parent.slider_widget().handle_dict_positions().keys())):
            i.setNum(index + 1)

        # self._parent.color_rect_scene().reverse_colors()
        self._parent.color_rect_scene().update_color_rect()


    def comp_chart(self):
        colors = [c.getRgbF() for c in self._parent.color_rect_scene().get_colors()]

        for index, c in enumerate(colors):
            new_color = 1 - c[0], 1 - c[1], 1 - c[2], c[3]
            colors[index] = new_color

        for index, key in enumerate(self._parent.slider_widget().handle_dict_positions()):
            key.setValue(colors[index])

        self._parent.color_rect_scene().update_color_rect()


    def black_body_setup(self):
        return [0,0.333, 0.666, 1], [(0,0,0), (1,0,0), (1,1,0), (1,1,1)], [1,1,1,1]

    def grayscale_setup(self):
        return [0,1], [(0,0,0),(1,1,1)], [1,1]

    def infra_red_setup(self):
        return [0, 0.25, 0.5, 0.75, 1], [(0.2,0,1),(0, 0.85, 1), (0,1, 0.1), (0.95, 1, 0), (1, 0, 0)], [1, 1, 1, 1, 1]

    def two_tone_setup(self):
        return [0, 0.5, 0.5, 0.5, 1], [(0, 1, 1), (0, 0, 1), (1, 0, 1), (1, 0, 0), (1, 1, 0)], [1, 1, 1, 1, 1]

    def white_to_red_setup(self):
        return [0,1], [(1, 1, 1), (1, 0, 0)], [1,1]



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
        self.move(0,30)
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
        return self.slider_positions.index(position)

    def removeHandle(self,index):
        self.slider_positions.pop(index)
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
        self.setFixedWidth(width)

    def update_height(self, height):
        self.move(0, height)


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
                self._current_control = itemlist[1]
                self._base_parent.widgetStack().setCurrentWidget(itemlist[1])
                return


    def mouseDoubleClickEvent(self, event) -> None:
        self._current_control.color_button_widget().openColorEditor()


    def mouseMoveEvent(self, event):
        distance = self.opt.maximum - self.opt.minimum
        pos = self.style().sliderValueFromPosition(0, distance, event.pos().x(), self.rect().width())

        if self._current_handle == QtWidgets.QStyle.SC_SliderHandle:
            self.slider_positions[self.currentIndex] = pos
            self._slider_pos_cont[self._current_control] = pos
            self.sort_dict_handles()

            itemlist = self._base_parent.itemData().getGroupB()[self.currentIndex]
            value = self._base_parent.mapRange_Clamp(pos,0,1000000.0, 0, 1)
            itemlist[1].setPosValue(value)

            for index, i in enumerate(list(self._slider_pos_cont.keys())):
                self._base_parent.color_rect_scene().update_range(index, self._base_parent.mapRange_Clamp(self._slider_pos_cont[i],0,1000000.0, 0, 1))
                i.setNum(index+1)

            self._base_parent.color_rect_scene().update_color_rect()
            self.update()
            return


    def moveSlider(self,index,pos, control):
        self.slider_positions[index] = pos
        self._slider_pos_cont[control] = pos
        self.update()



class PointNumWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(PointNumWidget, self).__init__()
        self._base_parent = parent
        self._other_parent = None
        self._base_index = 0

        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 5, 0, 5)
        self._layout.setAlignment(QtCore.Qt.AlignLeft)

        self._index_widget = LineEditWidgets.LineEditIntWidgetClass(no_num_button=False)
        self._index_widget.baseWidget().setToolTip('Mouse wheel to change Selection.')
        self._index_widget.baseWidget().setStyleSheet(
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

        self._add_button.pressed.connect(self.new_insert)
        self._sub_button.pressed.connect(self.remove_point)
        self._index_widget.baseWidget().valueChanged.connect(self.updateSelection)

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
        if self._index_widget.wheelState():
            self._index_widget.setValue(self._base_index)
            controls = list(self._base_parent.slider_widget().handle_dict_positions().keys())
            self._base_parent.widgetStack().setCurrentWidget(controls[value-1])
            self.setFocus()


    def new_insert(self):
        itemlist = self._base_parent.itemData().getGroupC()[self._other_parent]
        ranges = self._base_parent.color_rect_scene().get_ranges()
        colors = self._base_parent.color_rect_scene().get_colors()
        color_index = itemlist[0]

        next_range = ranges[color_index+1] if color_index < (len(ranges)-1) else ranges[color_index-1]
        next_color = colors[color_index+1] if color_index < (len(colors)-1) else colors[color_index-1]
        index = self._other_parent.number() if color_index < (len(colors)-1) else self._other_parent.number() - 1

        new_range = (ranges[itemlist[0]] + next_range) / 2
        new_color = tuple((x + y) / 2 for x, y in zip(colors[color_index].getRgbF(), next_color.getRgbF()))
        new_interp = self._other_parent.current_interpolation_index()

        color_obj = self._base_parent.color_ramp_setup(index, new_range, new_color, new_interp)
        self._base_parent.color_rect_scene().insert_range(index, new_range)
        self._base_parent.color_rect_scene().insert_color(index, color_obj)
        self._base_parent.color_rect_scene().update_color_rect()

        for index, i in enumerate(list(self._base_parent.slider_widget().handle_dict_positions().keys())):
            i.setNum(index + 1)


    def remove_point(self):
        itemlist = self._base_parent.itemData().getGroupC()[self._other_parent]

        self._base_parent.color_rect_scene().remove_color_data(itemlist[0])
        self._base_parent.itemData().removeGroupItems(self._other_parent)
        self._base_parent.itemData().update_indexs(itemlist[0], sub)
        self._base_parent.slider_widget().removeHandle(itemlist[1])
        self._base_parent.widgetStack().removeWidget(self._other_parent)
        self._other_parent.deleteLater()

        for i in range(0, self._base_parent.widgetStack().count()):
            widget = self._base_parent.widgetStack().widget(i)
            widget.setNum(i + 1)
            widget.setMaxNum(self._base_parent.widgetStack().count())

        self._base_parent.color_rect_scene().update_color_rect()



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
        self._interp_index = 0
        self._block_values = False

        self._num_widget = PointNumWidget(parent)
        self._num_widget.setControllerParent(self)

        self._pos_slider = SliderWidgetClass.FloatSliderWidget()
        self._pos_slider.setRange(0, 1 * 1000000.0)

        self._color_hor_layout = QtWidgets.QHBoxLayout()
        self._color_hor_layout.setSpacing(3)
        self._color_hor_layout.setContentsMargins(0, 0, 0, 0)
        self._color_hor_layout.setAlignment(QtCore.Qt.AlignLeft)

        self._r = LineEditWidgets.LineEditFloatWidgetClass(steps=0.1)
        self._r.setRange(0, 1)
        r_hint_widget = self._r.addHint('R')
        r_hint_widget.setProperty('class', 'x_property')

        self._g = LineEditWidgets.LineEditFloatWidgetClass(steps=0.1)
        self._g.setRange(0, 1)
        g_hint_widget = self._g.addHint('G')
        g_hint_widget.setProperty('class', 'y_property')

        self._b = LineEditWidgets.LineEditFloatWidgetClass(steps=0.1)
        self._b.setRange(0, 1)
        b_hint_widget = self._b.addHint('B')
        b_hint_widget.setProperty('class', 'z_property')

        self._color_button = ColorWidgetClass.ColorButtonWidget(self, False)

        self._color_hor_layout.addWidget(self._color_button)
        self._color_hor_layout.addWidget(self._r)
        self._color_hor_layout.addWidget(self._g)
        self._color_hor_layout.addWidget(self._b)

        self._r.baseWidget().valueChanged.connect(self._color_button.colorPickerWidget()._colorEdited)
        self._g.baseWidget().valueChanged.connect(self._color_button.colorPickerWidget()._colorEdited)
        self._b.baseWidget().valueChanged.connect(self._color_button.colorPickerWidget()._colorEdited)

        self._menu_interp = ComboBoxWidgetClass.ComboBoxWidget()
        self._menu_interp.addItems(
            ['Constant', 'Linear', 'Catmull-Rom', 'Monotone-Cubic', 'Bezier', 'B-Spline', 'Hermite'])

        self.withLabel('Point No.', self._num_widget)
        self.withLabel('Position', self._pos_slider)
        self.withLabel('Color', self._color_hor_layout)
        self.withLabel('Interpolation', self._menu_interp)

        self.setLayout(self._layout)

        self._pos_slider.slider.valueChanged.connect(self.updatePosition)
        self._menu_interp._combo_box.activated.connect(self.updatePath)


    def set_block(self, state: bool):
        self._block_values = state

    def color_button_widget(self):
        return self._color_button

    def withLabel(self, text, widget_obj):
        hor_layout = QtWidgets.QHBoxLayout()
        hor_layout.setSpacing(5)
        hor_layout.setContentsMargins(0, 0, 0, 0)

        hor_layout.addWidget(QtWidgets.QLabel(text=text))

        if isinstance(widget_obj, QtWidgets.QWidget):
            hor_layout.addWidget(widget_obj)
        else:
            hor_layout.addLayout(widget_obj)

        self._layout.addLayout(hor_layout)

    def updatePath(self, index):
        self._interp_index = index
        itemlist = self._parent.itemData().getGroupC()[self]
        # self._parent.graphicScene().updateInterp(itemlist[0], index)


    def current_interpolation_index(self):
        return self._interp_index


    def changeSelection(self, value):
        if self._notSelf:
            self._parent.widgetStack().setCurrentIndex(value - 1)
            other = self._parent.widgetStack().currentWidget()
            itemlist = self._parent.itemData().getGroupC()[other]
            itemlist[0].parentScene().itemSelect(itemlist[0])
            self.setNum(self._base_num)


    def updatePosition(self, value):
        if self._parent.bInit() and not self._block_values:
            itemlist = self._parent.itemData().getGroupC()[self]
            self._parent.slider_widget().moveSlider(itemlist[1], value, self)
            value = self._parent.mapRange_Clamp(value,0,1000000, 0, 1)
            self._parent.slider_widget().sort_dict_handles()

            for index, i in enumerate(list(self._parent.slider_widget().handle_dict_positions().keys())):
                i.setNum(index+1)

            self._parent.color_rect_scene().update_range(itemlist[0], value)
            self._parent.color_rect_scene().update_color_rect()

    def position_value(self):
        return self._pos_slider.value()

    def number(self):
        return self._num_widget._index_widget.value()

    def setNum(self, number: int):
        self._num_widget.setBase(number)

    def setMaxNum(self, max_num: int):
        self._num_widget.setRange(max_num)

    def setPosValue(self, position: float):
        self._pos_slider.setValue(position)

    def setInterp(self, index: int):
        self._interp_index = index
        self._menu_interp.setItem(index)

    def set_rgb(self, color):
        self._r.setValue(float(color[0]))
        self._g.setValue(float(color[1]))
        self._b.setValue(float(color[2]))

    def setValue(self, color):
        self._r.setValue(float(color[0]))
        self._g.setValue(float(color[1]))
        self._b.setValue(float(color[2]))

        if self in self._parent.itemData().getGroupC() and not self._block_values:
            color_obj = QtGui.QColor()
            color_obj.setRgbF(float(color[0]), float(color[1]), float(color[2]))
            itemlist = self._parent.itemData().getGroupC()[self]
            self._parent.color_rect_scene().update_color(itemlist[0], color_obj)
            self._parent.color_rect_scene().update_color_rect()


    def eval(self):
        return self._r.value(), self._g.value(), self._b.value()



class RampGraphicDisplayOuter(QtWidgets.QWidget):

    def __init__(self, parent):
        super(RampGraphicDisplayOuter, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(5, 0, 5, 10)

        self._parent = parent
        self._display_height = 40
        self.__doOnce = True

        self.setFixedHeight(self._display_height + 15)

        self._color_ramp = ColorRect(parent)

        self._layout.addWidget(self._color_ramp)
        self.setLayout(self._layout)


    def resizeEvent(self, event) -> None:
        self._color_ramp.update_width(self.size().width())
        self._parent.updateSlider_width(self.size().width())

        if self.__doOnce:
            self.__doOnce = False
            if not self._parent.itemData().getGroupA():
                self._parent.setRamp(*self._parent.actionButtons().grayscale_setup())


    def color_rect(self):
        return self._color_ramp




class ColorRect(QtWidgets.QWidget):

    def __init__(self, parent):
        super(ColorRect, self).__init__()
        self.setMaximumHeight(40)
        self.setMinimumHeight(40)
        self._parent = parent

        self._width = 398

        self._frame_colors = []
        self._color_ranges = []

        self.linearGrad = QtGui.QLinearGradient(5, 5, self._width, 25)
        self.linearBrush = QtGui.QBrush(self.linearGrad)


    def update_width(self, width):
        self._width = width
        self.update()


    def mousePressEvent(self, event) -> None:
        pass

    def clear_colors(self):
        self._color_ranges.clear()
        self._frame_colors.clear()

    def reverse_colors(self):
        self._color_ranges = self._color_ranges[::-1]
        self._frame_colors = self._frame_colors[::-1]


    def set_color_rect_values(self, colors, ranges):
        self._frame_colors = colors
        self._color_ranges = ranges
    
    def remove_color_data(self,index):
        self._color_ranges.pop(index)
        self._frame_colors.pop(index)
    
    def insert_range(self,index, range_value):
        self._color_ranges.insert(index, range_value)

    def insert_color(self,index, color):
        self._frame_colors.insert(index, color)

    def update_range(self,index, range_value):
        if index < len(self._color_ranges):
            self._color_ranges[index] = range_value

    def update_color(self, index, color):
        if index < len(self._frame_colors):
            self._frame_colors[index] = color

    def get_ranges(self):
        return self._color_ranges

    def get_colors(self):
        return self._frame_colors

    def paintEvent(self, event) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(self.linearBrush)
        painter.drawRect(0, 0, self._width, 40)

    def update_color_rect(self):
        self.linearGrad = QtGui.QLinearGradient(5, 5, self._width, 25)

        for i, c in enumerate(self._frame_colors):
            self.linearGrad.setColorAt(self._color_ranges[i], c)

        self.linearBrush = QtGui.QBrush(self.linearGrad)
        self.update()