from PySide2 import QtWidgets, QtCore
from PySideLayoutTool.UIEditorLib import LayoutTemplate, TemplateBuildClass, UIEditorFactory
from . import ColorWidgetClass
from ..LineEditTemplate import LineEditWidgets


class ColorSetupClass(LayoutTemplate.ParmSetup):

    def __init__(self, parent,useAlpha=False):
        super(ColorSetupClass, self).__init__(parent)
        self._hor_layout = QtWidgets.QHBoxLayout()
        self._hor_layout.setSpacing(3)
        self._hor_layout.setContentsMargins(0, 0, 0, 0)
        self._hor_layout.setAlignment(QtCore.Qt.AlignLeft)

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

        self._color_button = ColorWidgetClass.ColorButtonWidget(self, useAlpha)

        self._hor_layout.addWidget(self._color_button)
        self._hor_layout.addWidget(self._r)
        self._hor_layout.addWidget(self._g)
        self._hor_layout.addWidget(self._b)

        self._layout.addLayout(self._hor_layout)

        self._r.baseWidget().valueChanged.connect(self._color_button.colorPickerWidget()._colorEdited)
        self._g.baseWidget().valueChanged.connect(self._color_button.colorPickerWidget()._colorEdited)
        self._b.baseWidget().valueChanged.connect(self._color_button.colorPickerWidget()._colorEdited)

        self._r.baseWidget().valueChanged.connect(self._color_changed)
        self._g.baseWidget().valueChanged.connect(self._color_changed)
        self._b.baseWidget().valueChanged.connect(self._color_changed)


    def _color_changed(self,arg):
        self.notify_expressions()

    def setValue(self, value):
        value = list(value)
        self._r.setValue(float(value[0]))
        self._g.setValue(float(value[1]))
        self._b.setValue(float(value[2]))

    def PostUpdate(self):
        pass

    def eval(self):
        return self._r.value(), self._g.value(), self._b.value()



class ColorAlphaSetupClass(ColorSetupClass):

    def __init__(self,parent):
        self._alpha = LineEditWidgets.LineEditFloatWidgetClass(steps=0.1)
        self._alpha.addHint('A')
        super(ColorAlphaSetupClass, self).__init__(parent,useAlpha=True)

        self._hor_layout.addWidget(self._alpha)
        self._alpha._digital_widget.valueChanged.connect(self._color_button.colorPickerWidget()._colorEdited)

    def setValue(self, value):
        super(ColorAlphaSetupClass, self).setValue(value)
        self._alpha.setValue(value[3])

    def eval(self):
        return self._r.value(), self._g.value(), self._b.value(), self._alpha.value()


class ColorBuildClass(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return ColorSetupClass


class ColorAlphaBuildClass(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return ColorAlphaSetupClass



def register():
    UIEditorFactory.WidgetFactory.register('Color', ColorBuildClass)
    UIEditorFactory.WidgetFactory.register('Color-Alpha', ColorAlphaBuildClass)