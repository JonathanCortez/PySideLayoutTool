from PySide2 import QtWidgets, QtCore
from PySideLayoutTool.UIEditorLib.UIEditorProperty import UIProperty
from PySideLayoutTool.UIEditorLib import LayoutTemplate, TemplateBuildClass, UIEditorFactory
from . import ButtonWidgetClass

# TODO: Need to fix to work properly when buttons/button is set to join horizontal

class SimpleButtonSetupClass(LayoutTemplate.ParmSetup):

    def __init__(self, parent):
        super(SimpleButtonSetupClass, self).__init__(parent)
        horizontal_Layout = QtWidgets.QHBoxLayout()
        horizontal_Layout.setSpacing(0)
        horizontal_Layout.setContentsMargins(0,2,0,2)
        horizontal_Layout.setAlignment(QtCore.Qt.AlignLeft)

        self._button_widget = ButtonWidgetClass.ButtonWidget()

        horizontal_Layout.addSpacing(55)
        horizontal_Layout.addWidget(self._button_widget)

        self._layout.addLayout(horizontal_Layout)

        self._button_widget.pressed.connect(self.button_action)


    def bLabel(self):
        return False

    def button_action(self):
        self.notify_expressions()

    def PostUpdate(self):
        super(SimpleButtonSetupClass, self).PostUpdate()
        self._button_widget.changeText(self.label())

    def eval(self):
        return None




class ButtonStripSetupClass(LayoutTemplate.ParmSetup):

    def __init__(self,parent):
        super(ButtonStripSetupClass, self).__init__(parent)
        self._button_widget = ButtonWidgetClass.ButtonStripWidget()
        self._bLabel = True

        self._layout.addWidget(self._button_widget)

    @UIProperty(metaWidget='ComboProperty',label='Button Type',category='Combo/Menu Items',
                defaults=['Normal (Menu Only, Single Selection)','Normal Mini (Mini Menu Only, Single Selection)' ,'Toggle (Field + Multiple Selection)'])
    def button_type(self):
        pass

    @UIProperty(metaWidget='DictionaryProperty',label='Items',category='Combo/Menu Items')
    def dict_keyValue(self):
        pass

    def bLabel(self):
        return self._bLabel

    def PreUpdate(self):
        if self.button_type().currentItem_index == 1:
            self._bLabel = False

        self._button_widget.typeStrip(self.button_type().currentItem_index)

    def PostUpdate(self):
        super(ButtonStripSetupClass, self).PostUpdate()
        if self._button_widget.layout().itemAt(0).count() > 0:
            for i in range(0,self._button_widget.layout().itemAt(0).count()):
                item_layout = self._button_widget.layout().itemAt(0).itemAt(i)
                widget = item_layout.widget()
                widget.deleteLater()

            self._button_widget.clearButtons()

        if self.button_type().currentItem_index != 1 and self.dict_keyValue().keys:
            if len(self.dict_keyValue().keys) > 0:
                self._button_widget.addButtons(self.dict_keyValue().keys)

    def eval(self):
        if self.button_type().currentItem_index == 2:
            return self._button_widget.checked_buttons()
        else:
            return self._button_widget.lastSelected()


class RGBAButtonWidgetSetup(LayoutTemplate.ParmSetup):

    def __init__(self, parent):
        super(RGBAButtonWidgetSetup, self).__init__(parent)
        self._button_widget = ButtonWidgetClass.RGBAButtonWidget()
        self._layout.addWidget(self._button_widget)

    def eval(self):
        return self._button_widget.rgb_button_state(), self._button_widget.red_button_state(), self._button_widget.green_button_state(), self._button_widget.blue_button_state(), self._button_widget.alpha_button_state()

    def PostUpdate(self):
        self._button_widget._rgb_button_widget.setToolTip('Toggle RGB')
        self._button_widget._rgb_button_widget.setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")

        self._button_widget._r_button_widget.setToolTip('Red')
        self._button_widget._r_button_widget.setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")

        self._button_widget._g_button_widget.setToolTip('Green')
        self._button_widget._g_button_widget.setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")

        self._button_widget._b_button_widget.setToolTip('Blue')
        self._button_widget._b_button_widget.setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")

        self._button_widget._a_button_widget.setToolTip('Alpha')
        self._button_widget._a_button_widget.setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")

    def set_value(self, value):
        pass




class SimpleButtonBuildClass(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return SimpleButtonSetupClass


class ButtonStripBuildClass(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return ButtonStripSetupClass


class ButtonRGBABuildClass(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return RGBAButtonWidgetSetup


def register():
    UIEditorFactory.WidgetFactory.register('Button', SimpleButtonBuildClass)
    UIEditorFactory.WidgetFactory.register('Button Strip', ButtonStripBuildClass)
    UIEditorFactory.WidgetFactory.register('RGBA Mask', ButtonRGBABuildClass)
