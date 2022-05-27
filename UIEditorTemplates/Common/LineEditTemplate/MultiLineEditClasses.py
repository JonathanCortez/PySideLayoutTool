from PySide2 import QtWidgets
from PySideLayoutTool.UIEditorLib.UIEditorProperty import UIProperty
from PySideLayoutTool.UIEditorLib import LayoutTemplate, TemplateBuildClass, UIEditorFactory
from . import LineEditWidgets
from collections import namedtuple


class VectorClasses(LayoutTemplate.ParmSetup):

    def __init__(self,parent):
        super(VectorClasses, self).__init__(parent)
        self._hor_layout = QtWidgets.QHBoxLayout()
        self._hor_layout.setSpacing(3)
        self._hor_layout.setContentsMargins(0, 0, 0, 0)

        self._layout.addLayout(self._hor_layout)

    @UIProperty(metaWidget='ClampProperty', label='Range', category='Setting')
    def clampRange(self):
        pass

#---------------------------------------------------------------------------------------------------------

class IntegerVector2Class(VectorClasses):

    def __init__(self,parent):
        super(IntegerVector2Class, self).__init__(parent)
        self._v1 = LineEditWidgets.LineEditIntWidgetClass()
        x_hint_widget = self._v1.addHint('X')
        x_hint_widget.setProperty('class', 'x_property')

        self._v2 = LineEditWidgets.LineEditIntWidgetClass()
        y_hint_widget = self._v2.addHint('Y')
        y_hint_widget.setProperty('class', 'y_property')

        self._value1, self._value2 = 0, 0
        value_tuple = namedtuple('Value',['x', 'y'])
        self._value = value_tuple(self._value1, self._value2)

        self._hor_layout.addWidget(self._v1)
        self._hor_layout.addWidget(self._v2)

        self._v1.baseWidget().valueChanged.connect(self._v1_change)
        self._v2.baseWidget().valueChanged.connect(self._v2_change)

    def _v1_change(self, arg):
        self._value1 = arg
        self.notify_expressions()

    def _v2_change(self, arg):
        self._value2 = arg
        self.notify_expressions()

    def PostUpdate(self):
        self._v1.setToolTip(f"<p style='white-space:pre'> Parameter: <B>{self.name() + '_x'}<B></p> {self.tooltip()} " if self.tooltip() != '' else f"<p style='white-space:pre'> Parameter: <B>{self.name() + '_x'}<B></p>")
        self._v2.setToolTip(f"<p style='white-space:pre'> Parameter: <B>{self.name() + '_y'}<B></p> {self.tooltip()} " if self.tooltip() != '' else f"<p style='white-space:pre'> Parameter: <B>{self.name() + '_y'}<B></p>")
        self._v1.setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")
        self._v2.setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")

        self._v1.setValue(self.clampRange().min)
        self._v2.setValue(self.clampRange().min)

        self._parent._widgets[self.name() + '_x'] = self._v1
        self._parent._widgets[self.name() + '_y'] = self._v2

    def eval(self):
        return self._value

    def set_value(self, value):
        value = list(value)
        self._value1 = int(value[0])
        self._value2 = int(value[1])

        self._v1.baseWidget().setValue(self._value1)
        self._v2.baseWidget().setValue(self._value2)



class IntegerVector3Class(IntegerVector2Class):

    def __init__(self,parent):
        super(IntegerVector3Class, self).__init__(parent)
        self._v3 = LineEditWidgets.LineEditIntWidgetClass()
        x_hint_widget = self._v3.addHint('Z')
        x_hint_widget.setProperty('class', 'z_property')

        self._value3 = 0
        value_tuple = namedtuple('Value', ['x', 'y', 'z'])
        self._value = value_tuple(self._value1, self._value2, self._value3)

        self._hor_layout.addWidget(self._v3)

        self._v3.baseWidget().valueChanged.connect(self._v3_change)

    def _v3_change(self,arg):
        self._value3 = arg
        self.notify_expressions()

    def PostUpdate(self):
        super(IntegerVector3Class, self).PostUpdate()
        self._v3.setToolTip(f"<p style='white-space:pre'> Parameter: <B>{self.name() + '_z'}<B></p> {self.tooltip()} " if self.tooltip() != '' else f"<p style='white-space:pre'> Parameter: <B>{self.name() + '_z'}<B></p>")
        self._v3.setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")

        self._v3.setValue(self.clampRange().min)

        self._parent._widgets[self.name() + '_z'] = self._v3

    def eval(self):
        return self._value

    def set_value(self, value):
        value = list(value)
        self._value1 = int(value[0])
        self._value2 = int(value[1])
        self._value3 = int(value[2])

        self._v1.baseWidget().setValue(self._value1)
        self._v2.baseWidget().setValue(self._value2)
        self._v3.baseWidget().setValue(self._value3)


class IntegerVector4Class(IntegerVector3Class):

    def __init__(self,parent):
        super(IntegerVector4Class, self).__init__(parent)
        self._v4 = LineEditWidgets.LineEditIntWidgetClass()
        self._v4.addHint('W')

        self._value4 = 0
        value_tuple = namedtuple('Value', ['x', 'y', 'z','w'])
        self._value = value_tuple(self._value1, self._value2, self._value3, self._value4)

        self._hor_layout.addWidget(self._v4)

        self._v4.baseWidget().valueChanged.connect(self._v4_change)


    def _v4_change(self, arg):
        self._value4 = arg
        self.notify_expressions()

    def PostUpdate(self):
        super(IntegerVector4Class, self).PostUpdate()
        self._v4.setToolTip(f"<p style='white-space:pre'> Parameter: <B>{self.name() + '_w'}<B></p> {self.tooltip()} " if self.tooltip() != '' else f"<p style='white-space:pre'> Parameter: <B>{self.name() + '_w'}<B></p>")
        self._v4.setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")

        self._v4.setValue(self.clampRange().min)

        self._parent._widgets[self.name() + '_w'] = self._v4

    def eval(self):
        return self._value

    def set_value(self, value):
        value = list(value)
        self._value1 = int(value[0])
        self._value2 = int(value[1])
        self._value3 = int(value[2])
        self._value4 = int(value[3])


        self._v1.baseWidget().setValue(self._value1)
        self._v2.baseWidget().setValue(self._value2)
        self._v3.baseWidget().setValue(self._value3)
        self._v4.baseWidget().setValue(self._value4)


#------------------------------------------------------------------------------------------------------------

class FloatVector2Class(VectorClasses):

    def __init__(self,parent):
        super(FloatVector2Class, self).__init__(parent)
        self._v1 = LineEditWidgets.LineEditFloatWidgetClass(steps=0.1)
        x_hint_widget = self._v1.addHint('X')
        x_hint_widget.setProperty('class', 'x_property')

        self._v2 = LineEditWidgets.LineEditFloatWidgetClass(steps=0.1)
        y_hint_widget = self._v2.addHint('Y')
        y_hint_widget.setProperty('class', 'y_property')

        self._value1, self._value2 = 0.0, 0.0
        value_tuple = namedtuple('Value',['x', 'y'])
        self._value = value_tuple(self._value1, self._value2)

        self._hor_layout.addWidget(self._v1)
        self._hor_layout.addWidget(self._v2)

        self._v1.baseWidget().valueChanged.connect(self._v1_change)
        self._v2.baseWidget().valueChanged.connect(self._v2_change)

    def _v1_change(self, arg):
        self._value1 = arg
        self.notify_expressions()

    def _v2_change(self, arg):
        self._value2 = arg
        self.notify_expressions()

    def PostUpdate(self):
        self._v1.setToolTip(f"<p style='white-space:pre'> Parameter: <B>{self.name() + '_x'}<B></p> {self.tooltip()} " if self.tooltip() != '' else f"<p style='white-space:pre'> Parameter: <B>{self.name() + '_x'}<B></p>")
        self._v2.setToolTip(f"<p style='white-space:pre'> Parameter: <B>{self.name() + '_y'}<B></p> {self.tooltip()} " if self.tooltip() != '' else f"<p style='white-space:pre'> Parameter: <B>{self.name() + '_y'}<B></p>")
        self._v1.setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")
        self._v2.setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")

        self._v1.setValue(self.clampRange().min * 1000000.0)
        self._v2.setValue(self.clampRange().min * 1000000.0)

        self._parent._widgets[self.name() + '_x'] = self._v1
        self._parent._widgets[self.name() + '_y'] = self._v2

    def eval(self):
        return self._value

    def set_value(self, value):
        value = list(value)
        self._value1 = float(value[0])
        self._value2 = float(value[1])

        self._v1.baseWidget().setValue(self._value1)
        self._v2.baseWidget().setValue(self._value2)


class FloatVector3Class(FloatVector2Class):

    def __init__(self,parent):
        super(FloatVector3Class, self).__init__(parent)
        self._v3 = LineEditWidgets.LineEditFloatWidgetClass(steps=0.1)
        x_hint_widget = self._v3.addHint('Z')
        x_hint_widget.setProperty('class', 'z_property')

        self._value3 = 0.0
        value_tuple = namedtuple('Value', ['x', 'y', 'z'])
        self._value = value_tuple(self._value1, self._value2, self._value3)

        self._hor_layout.addWidget(self._v3)

        self._parent._widgets[self.name() + '_z'] = self._v3

        self._v3.baseWidget().valueChanged.connect(self._v3_change)

    def _v3_change(self, arg):
        self._value3 = arg
        self.notify_expressions()

    def PostUpdate(self):
        super(FloatVector3Class, self).PostUpdate()
        self._v3.setToolTip(f"<p style='white-space:pre'> Parameter: <B>{self.name() + '_z'}<B></p> {self.tooltip()} " if self.tooltip() != '' else f"<p style='white-space:pre'> Parameter: <B>{self.name() + '_z'}<B></p>")
        self._v3.setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")

        self._v3.setValue(self.clampRange().min * 1000000.0)

        self._parent._widgets[self.name() + '_z'] = self._v3

    def eval(self):
        return self._value

    def set_value(self, value):
        value = list(value)
        self._value1 = float(value[0])
        self._value2 = float(value[1])
        self._value3 = float(value[2])


        self._v1.baseWidget().setValue(self._value1)
        self._v2.baseWidget().setValue(self._value2)
        self._v3.baseWidget().setValue(self._value3)



class FloatVector4Class(FloatVector3Class):

    def __init__(self,parent):
        super(FloatVector4Class, self).__init__(parent)
        self._v4 = LineEditWidgets.LineEditFloatWidgetClass(steps=0.1)
        self._v4.addHint('W')

        self._value4 = 0.0
        value_tuple = namedtuple('Value', ['x', 'y', 'z','w'])
        self._value = value_tuple(self._value1, self._value2, self._value3, self._value4)

        self._hor_layout.addWidget(self._v4)

        self._v4.baseWidget().valueChanged.connect(self._v4_change)

    def _v4_change(self, arg):
        self._value4 = arg
        self.notify_expressions()

    def PostUpdate(self):
        super(FloatVector4Class, self).PostUpdate()
        self._v4.setToolTip(f"<p style='white-space:pre'> Parameter: <B>{self.name() + '_w'}<B></p> {self.tooltip()} " if self.tooltip() != '' else f"<p style='white-space:pre'> Parameter: <B>{self.name() + '_w'}<B></p>")
        self._v4.setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")

        self._v4.setValue(self.clampRange().min * 1000000.0)

        self._parent._widgets[self.name() + '_w'] = self._v4

    def eval(self):
        return self._value

    def set_value(self, value):
        value = list(value)
        self._value1 = float(value[0])
        self._value2 = float(value[1])
        self._value3 = float(value[2])
        self._value4 = float(value[3])

        self._v1.baseWidget().setValue(self._value1)
        self._v2.baseWidget().setValue(self._value2)
        self._v3.baseWidget().setValue(self._value3)
        self._v4.baseWidget().setValue(self._value4)


#----------------------------------------------------------------------------------------------------

class V2IntegerClass(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return IntegerVector2Class


class V3IntegerClass(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return IntegerVector3Class


class V4IntegerClass(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return IntegerVector4Class


#---------------------------------------------------------------------------------------------------

class V2FloatClass(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return FloatVector2Class


class V3FloatClass(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return FloatVector3Class


class V4FloatClass(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return FloatVector4Class


#------------------------------------------------------------------------------------------------


def register():
    UIEditorFactory.WidgetFactory.register('Integer Vector 2', V2IntegerClass)
    UIEditorFactory.WidgetFactory.register('Integer Vector 3', V3IntegerClass)
    UIEditorFactory.WidgetFactory.register('Integer Vector 4', V4IntegerClass)

    UIEditorFactory.WidgetFactory.register('Float Vector 2', V2FloatClass)
    UIEditorFactory.WidgetFactory.register('Float Vector 3', V3FloatClass)
    UIEditorFactory.WidgetFactory.register('Float Vector 4', V4FloatClass)