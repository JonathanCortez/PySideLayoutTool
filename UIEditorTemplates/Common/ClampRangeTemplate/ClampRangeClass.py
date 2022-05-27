from PySideLayoutTool.UIEditorLib.UIEditorProperty import UIProperty
from PySideLayoutTool.UIEditorLib import LayoutTemplate, TemplateBuildClass, UIEditorFactory
from . import ClampRangeWidgetClass


class RangeWidgetSetup(LayoutTemplate.ParmSetup):

    def __init__(self, parent, bInt=True):
        super(RangeWidgetSetup, self).__init__(parent)
        self._range_widget = ClampRangeWidgetClass.ClampRangeWidget(0,10, False, False, bInt)
        self._layout.addWidget(self._range_widget)

        self._range_widget.minEdit_widget.valueChanged.connect(self._range_widget_changed)
        self._range_widget.maxEdit_widget.valueChanged.connect(self._range_widget_changed)
        self._range_widget.minLock_widget.pressed.connect(self._range_widget_changed)
        self._range_widget.maxLock_widget.pressed.connect(self._range_widget_changed)

    @UIProperty(metaWidget='ClampProperty', label='Range', category='Setting')
    def clampRange(self):
        pass

    def _range_widget_changed(self):
        self.notify_expressions()

    def PostUpdate(self):
        self._range_widget.minEdit_widget.setToolTip(f"<p style='white-space:pre'> Parameter: <B>{self.name() + '_min'}<B></p> {self.tooltip()} " if self.tooltip() != '' else f"<p style='white-space:pre'> Parameter: <B>{self.name() + '_min'}<B></p>")
        self._range_widget.minEdit_widget.setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")

        self._range_widget.maxEdit_widget.setToolTip(f"<p style='white-space:pre'> Parameter: <B>{self.name() + '_max'}<B></p> {self.tooltip()} " if self.tooltip() != '' else f"<p style='white-space:pre'> Parameter: <B>{self.name() + '_max'}<B></p>")
        self._range_widget.maxEdit_widget.setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")

        self._range_widget.minEdit_widget.setRange(self.clampRange().min if self.clampRange().minLock else -1000000,self.clampRange().max if self.clampRange().maxLock else 1000000)
        self._range_widget.maxEdit_widget.setRange(self.clampRange().min if self.clampRange().minLock else -1000000,self.clampRange().max if self.clampRange().maxLock else 1000000)

        self._range_widget.minEdit_widget.setValue(self.clampRange().min)
        self._range_widget.maxEdit_widget.setValue(self.clampRange().max)
        self._range_widget.minLock_widget.setChecked(self.clampRange().minLock)
        self._range_widget.maxLock_widget.setChecked(self.clampRange().maxLock)

        self._parent._widgets[self.name() + '_min'] = self._range_widget.minEdit_widget
        self._parent._widgets[self.name() + '_max'] = self._range_widget.minEdit_widget


    def eval(self):
        return self._range_widget.minEdit_widget.value(), self._range_widget.maxEdit_widget.value(), self._range_widget.minLock_widget.isChecked(), self._range_widget.maxLock_widget.isChecked()



class FloatRangeWidgetSetup(RangeWidgetSetup):

    def __init__(self,parent):
        super(FloatRangeWidgetSetup, self).__init__(parent, False)



class IntRangeWidgetBuildClass(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return RangeWidgetSetup

class FloatRangeWidgetBuildClass(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return FloatRangeWidgetSetup



def register():
    UIEditorFactory.WidgetFactory.register('Min/Max Integer', IntRangeWidgetBuildClass)
    UIEditorFactory.WidgetFactory.register('Min/Max Float', FloatRangeWidgetBuildClass)