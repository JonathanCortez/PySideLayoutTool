from abc import abstractmethod
from typing import Any

from PySideLayoutTool.UIEditorLib.UIEditorProperty import UIProperty
from PySideLayoutTool.UIEditorLib import LayoutTemplate, TemplateBuildClass, UIEditorFactory
from PySide2 import QtWidgets
from . import SliderWidgetClass

class SliderTemplateClass(LayoutTemplate.ParmSetup):

    def __init__(self,parent,bFloat=True):
        super(SliderTemplateClass, self).__init__(parent)
        self._value = 0
        self._slider_widget = SliderWidgetClass.FloatSliderWidget() if bFloat else SliderWidgetClass.IntSliderWidget()
        self._layout.addWidget(self._slider_widget)

        self._slider_widget.slider.valueChanged.connect(self._set_slider_value)
        self._slider_widget.boxEdit._digital_widget.editingFinished.connect(self._set_box_value)
        self._slider_widget.boxEdit._digital_widget.valueChanged.connect(self._wheel_set_box_value)

    def clamp(self, num, min_value, max_value):
        return max(min(num,max_value),min_value)
    
    def eval(self):
        return self._value

    @abstractmethod
    def set_value(self, value):
        pass

    @abstractmethod
    def setting(self, settings: Any):
        """ Give parameter set of values. """

    @abstractmethod
    def _set_slider_value(self, value):
        """ Set Text to Slider value."""
        self.notify_expressions()

    @abstractmethod
    def _set_box_value(self):
        """ Set Slider value to Text. """
        self.notify_expressions()

    @abstractmethod
    def _wheel_set_box_value(self):
        self.notify_expressions()


class IntegerSliderClass(SliderTemplateClass):
    def __init__(self,parent):
        super(IntegerSliderClass, self).__init__(parent,bFloat=False)
        pass

    @UIProperty(metaWidget='ClampProperty', label='Range', category='Setting')
    def clampRange(self):
        pass

    def set_value(self, value):
        self._value = int(value)
        self._set_slider_value(self._value)

    def PostUpdate(self):
        super(IntegerSliderClass, self).PostUpdate()
        self._value = int(self.clampRange().min)
        self._slider_widget.slider.setRange(self.clampRange().min, self.clampRange().max)
        self._slider_widget.slider.setValue(self._value)
        self._slider_widget.slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self._slider_widget.slider.setTickInterval(1)
        self._slider_widget.boxEdit.setRange(int(self.clampRange().min) if self.clampRange().minLock else -1000000, int(self.clampRange().max) if self.clampRange().maxLock else 1000000)
        self._slider_widget.boxEdit.setValue(self._value)


    def _set_slider_value(self, value):
        if self._slider_widget._slider_block:
            if self._value != value:
                self._slider_widget._boxedit_block = False
                self._value = self.clamp(value, int(self.clampRange().min  * 1000000.0) if self.clampRange().minLock else -100000000, int(self.clampRange().max * 1000000.0) if self.clampRange().maxLock else 100000000)
                self._slider_widget.boxEdit.setValue(value)
                self._slider_widget._boxedit_block = True
                super()._set_slider_value(self._value)



    def _set_box_value(self):
        if self._slider_widget._boxedit_block:
            self._slider_widget._slider_block = False
            self._value = self.clamp(self._slider_widget.boxEdit.value(), int(self.clampRange().min * 1000000.0) if self.clampRange().minLock else -100000000,int(self.clampRange().max * 1000000.0) if self.clampRange().maxLock else 100000000)
            self._slider_widget.slider.setValue(self._value)
            self.setFocus()
            self._slider_widget._slider_block = True
            super()._set_box_value()

    def _wheel_set_box_value(self):
        if self._slider_widget.boxEdit.wheelState():
            self._slider_block = False
            self._boxedit_block = False
            self._value = self._slider_widget.boxEdit.value()
            self._slider_widget.slider.setValue(self._value)
            self._slider_block = True
            self._boxedit_block = True
            super()._set_box_value()



class FloatSliderClass(SliderTemplateClass):
    def __init__(self,parent):
        super(FloatSliderClass, self).__init__(parent)
        pass

    @UIProperty(metaWidget='ClampProperty', label='Range', category='Setting', defaults=(0, 10, False, False, False))
    def clampRange(self):
        pass

    def set_value(self, value):
        self._value = float(value)
        self._set_slider_value(self._value)

    def PostUpdate(self):
        super(FloatSliderClass, self).PostUpdate()
        self._value = float(self.clampRange().min)
        self._slider_widget.slider.setRange(int(self.clampRange().min * 1000000.0),int(self.clampRange().max * 1000000.0))
        self._slider_widget.slider.setValue(int(self._value * 1000000.0))
        self._slider_widget.boxEdit.setRange(float(self.clampRange().min) if self.clampRange().minLock else -1000000.0, float(self.clampRange().max) if self.clampRange().maxLock else 1000000.0)
        self._slider_widget.boxEdit.setValue(float(self._value))


    def _set_slider_value(self, value):
        if self._slider_widget._slider_block:
            if self._value != value:
                self._slider_widget._boxedit_block = False
                self._value = float(self.clamp(value, int(self.clampRange().min  * 1000000.0) if self.clampRange().minLock else -100000000, int(self.clampRange().max * 1000000.0) if self.clampRange().maxLock else 100000000) / 1000000.0)
                self._slider_widget.boxEdit.setValue(round(self._value, 3))
                self._slider_widget._boxedit_block = True
                super()._set_slider_value(self._value)


    def _set_box_value(self):
        if self._slider_widget._boxedit_block:
            self._slider_widget._slider_block = False
            self._value = self._slider_widget.boxEdit.value() # float(self.clamp(self._slider_widget.boxEdit.value(), int(self.clampRange().min * 1000000.0) if self.clampRange().minLock else -100000000,int(self.clampRange().max * 1000000.0) if self.clampRange().maxLock else 100000000) / 1000000.0)
            self._slider_widget.slider.setValue(int(1000000.0 * self._value))
            self.setFocus()
            self._slider_widget._slider_block = True
            super()._set_box_value()


    def _wheel_set_box_value(self):
        if self._slider_widget.boxEdit.wheelState():
            self._slider_block = False
            self._boxedit_block = False
            self._value = self._slider_widget.boxEdit.value()
            self._slider_widget.slider.setValue(int(1000000.0 * self._value))
            self._slider_block = True
            self._boxedit_block = True
            super()._set_box_value()




class IntegerClass(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return IntegerSliderClass



class FloatClass(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return FloatSliderClass
    


def register():
    UIEditorFactory.WidgetFactory.register('Integer', IntegerClass)
    UIEditorFactory.WidgetFactory.register('Float', FloatClass)
