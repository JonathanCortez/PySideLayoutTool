import ast

from PySideLayoutTool.UIEditorLib.UIEditorProperty import UIProperty
from PySideLayoutTool.UIEditorLib import LayoutTemplate, TemplateBuildClass, UIEditorFactory
from . import RampWidgetClass, RampColorWidgetClass

class RampSetupClass(LayoutTemplate.ParmSetup):

    def __init__(self,parent):
        super(RampSetupClass, self).__init__(parent)
        self._ramp_widget = RampWidgetClass.RampWidgetSetup(self)
        self._layout.addWidget(self._ramp_widget)

    @UIProperty(metaWidget='ComboProperty',label='Def Interpolation',category='Default',
                defaults=['Constant','Linear','Catmull-Rom','Monotone Cubic', 'Bezier', 'B-Spline', 'Hermit'])
    def default_interp(self):
        pass

    def bLabel(self) -> bool:
        return False

    def PostUpdate(self):
        self._ramp_widget.label(self.label())

    def set_value(self, value):
        value = ast.literal_eval(value)
        positions = list(map(int, list(value['positions'])))
        values = list(map(int, list(value['values'])))
        interpolations = list(map(int, list(value['interpolations'])))
        self._ramp_widget.setRamp(positions,values,interpolations)

    def eval(self):
        return self._ramp_widget.get_ramp()




class RampColorSetupClass(LayoutTemplate.ParmSetup):

    def __init__(self,parent):
        super(RampColorSetupClass, self).__init__(parent)
        self._ramp_widget = RampColorWidgetClass.RampColorWidgetSetup(self)
        self._layout.addWidget(self._ramp_widget)

    def bLabel(self) -> bool:
        return False

    def PostUpdate(self):
        self._ramp_widget.label(self.label())



class RampBuildClass(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return RampSetupClass


class RampColorBuildClass(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return RampColorSetupClass



def register():
    UIEditorFactory.WidgetFactory.register('Ramp (Float)', RampBuildClass)
    UIEditorFactory.WidgetFactory.register('Ramp (Color)', RampColorBuildClass)