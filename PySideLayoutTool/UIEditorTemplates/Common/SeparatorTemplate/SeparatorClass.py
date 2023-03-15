from PySideLayoutTool.UIEditorLib import LayoutTemplate, TemplateBuildClass, UIEditorIconFactory
from PySideLayoutTool.UIEditorLib.UIEditorFactory import WidgetFactory
from PySideLayoutTool.UIEditorLib.UIEditorProperty import UIProperty
from PySide2 import QtWidgets
from . import SeparatorWidgetClass

class SeparatorClass(LayoutTemplate.ParmSetup):
    def __init__(self,parent):
        super(SeparatorClass, self).__init__(parent)
        self._sep = SeparatorWidgetClass.SeparatorHWidget()
        self._textLabel = QtWidgets.QLabel(text='None')
        self._textLabel.setVisible(self.bUseLabel())

        self._Hlayout = QtWidgets.QHBoxLayout()
        self._sep.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self._Hlayout.addWidget(self._textLabel)
        self._Hlayout.addSpacing(5)
        self._Hlayout.addWidget(self._sep)
        self._Hlayout.setContentsMargins(0, 0, 0, 0)
        self._layout.addLayout(self._Hlayout)


    def PostUpdate(self):
        self._textLabel.setVisible(self.bUseLabel())
        if self.bUseLabel():
            self._textLabel.setText(self.label())

    @UIProperty(metaWidget='CheckProperty', label='Use Label', category='Setting')
    def bUseLabel(self):
        pass

    def bLabel(self):
        return False

    def eval(self):
        return None


class SeparatorBase(TemplateBuildClass.ParameterBuild):

    def prefixStart_name(self) -> str:
        return 'sepparm'

    def prefixStart_label(self) -> str:
        return 'Separator'

    def widgetClass(self):
        return SeparatorClass

    def set_icon(self) -> None:
        return UIEditorIconFactory.IconEditorFactory.create('separtor_v1')

def register() -> None:
    WidgetFactory.register('Separator', SeparatorBase)
