from __future__ import annotations

from PySide2 import QtWidgets
from PySide2.QtCore import QObject, Signal

from abc import abstractmethod

from . import StringValidatorClass, TemplateDataClass
from .UIEditorProperty import ProcessUIProperties, UIProperty
from . import UIFunctions as ui



try:
    import unreal
except ImportError:
    pass


class CallbackObject(QObject):
    callback = Signal()


class WidgetSetup(QtWidgets.QWidget):
    """ Widget base class """


    def __init__(self, parent):
        super(WidgetSetup, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._parent = parent

        self.setLayout(self._layout)

        self._signal = CallbackObject()

        self._layout_parent = None
        self._label_widget = None
        self._observingObjs = []
        self._delegate_objs = []

        self._id = -1
        self._parent_id = -1
        self._is_child_widget = False

        self._hidden_str_list = None
        self._disable_str_list = None

        self._signal.callback.connect(self.callback_func) #type: ignore


    @classmethod
    @ProcessUIProperties
    def _displayProperties(self):
        pass

    def _pass_instances(self, widget_instances):
        names = getattr(self.__class__, '__UIProperties__')
        for attribute in dir(self.__class__):
            if attribute in names:
                for instance in widget_instances:
                    if attribute == instance.func_owner:
                        if not hasattr(self, '__property_instances__'):
                            new_dict = {attribute: instance.property_widget}
                            setattr(self, '__property_instances__', new_dict)
                        else:
                            getattr(self, '__property_instances__')[attribute] = instance.property_widget



    def _updateProperties(self):
        names = getattr(self.__class__, '__UIProperties__')
        for attribute in dir(self.__class__):
            if attribute in names:
                attribute_value = getattr(self.__class__, attribute)
                attribute_value._init_update(self)


    def notify_expressions(self):
        for delegate in self._delegate_objs:
            delegate(self.name(), self.eval())

        for observer in self._observingObjs:
            observer.notify_conditions()

        self.callback_func()


    def callback_func(self):
        if hasattr(self,'__code_obj__') :
            exec(compile(getattr(self, '__code_obj__'), 'Script', 'exec'), globals(), locals())
            if hasattr(self, '__call_obj__'):
                if hasattr(self, '__call_args__'):
                    locals()['kwargs'] = getattr(self, '__call_args__')
                exec(compile(getattr(self, '__call_obj__'), 'Script', 'exec'), globals(), locals())



    def notify_conditions(self):
        self._disable_implementation(self._eval_expression(self._disable_str_list) if self._disable_str_list is not None else False)
        self._hidden_implementation(self._eval_expression(self._hidden_str_list) if self._hidden_str_list is not None else False)

    def _eval_expression(self, expression) -> bool:
        expressionStr = ''
        expressionStr = ' '.join([str(elem.eval() if isinstance(elem, QtWidgets.QWidget) else elem) for elem in expression])
        return eval(expressionStr)


    def _setHidden_expression(self, expressionList):
        self._hidden_str_list = expressionList

    def _setDisable_expression(self, expressionList):
        self._disable_str_list = expressionList

    def _disable_implementation(self, state: bool):
        self.setDisabled(state)
        if self._layout_parent:
            self._layout_parent.itemAt(0).widget().setDisabled(state)

    def _hidden_implementation(self, state: bool):
        self.setHidden(state)
        if self._layout_parent:
            self._layout_parent.itemAt(0).widget().setHidden(state)

    def add_delegate(self, func):
        self._delegate_objs.append(func)
        
    def remove_delegate(self, func):
        if func in self._delegate_objs:
            self._delegate_objs.pop(func)

    def add_Observer(self, widget_obj: WidgetSetup) -> None:
        self._observingObjs.append(widget_obj)

    def clear_Observers(self):
        self._observingObjs.clear()

    def set_label_widget(self, widget_label):
        self._label_widget = widget_label

    def set_layout_parent(self, layout_parent):
        self._layout_parent = layout_parent

    def layout_win(self):
        return self._parent
    # @property
    # def parent_id(self):
    #     return self._parent_id
    #
    # @parent_id.setter
    # def parent_id(self, parent_id: int):
    #     self._parent_id = parent_id
    #
    # @property
    # def is_child(self):
    #     return self._is_child_widget
    #
    # @is_child.setter
    # def is_child(self, state: bool):
    #     self._is_child_widget = state
    #
    # @property
    # def widget_id(self):
    #     return self._id
    #
    # @widget_id.setter
    # def widget_id(self, id_num: int):
    #     self._id = id_num


    @UIProperty(metaWidget='LineEditProperty', label='Name', category='Default', category_args=(True,300), defaults=(2, 1,'NewName',StringValidatorClass.checkString))
    def name(self):
        pass


    @UIProperty(metaWidget='LineEditProperty', label='Label', category='Default', use_separator=True)
    def label(self):
        pass


    @UIProperty(metaWidget='LineEditProperty', label='Callback Script', category='Default', use_separator=True)
    def callback(self):
        """ callback for conditions and script call given. """


    @UIProperty(metaWidget='ComboProperty', label='Type', category='Default', use_separator=True)
    def type(self):
        """ String representation of what type this widget is."""
    
    @UIProperty(metaWidget='LineEditProperty', label='Help', category='Default')
    def tooltip(self):
        pass

    @UIProperty(metaWidget='LineEditProperty', label='Disable When', category='Expressions')
    def disable_when(self):
        pass


    @UIProperty(metaWidget='LineEditProperty', label='Hide When', category='Expressions')
    def hiden_when(self):
        pass


    @UIProperty(metaWidget='CheckProperty', label='Invisible', category='Setting')
    def invisible(self):
        pass

    @abstractmethod
    def PreUpdate(self):
        """ stuff before adding to the layout."""

    @abstractmethod
    def PostUpdate(self):
        """ Handle how widgets get updated """
        tooltip_string = f"<p style='white-space:pre'> Parameter: <B>{self.name()}<B></p> {self.tooltip()} " if self.tooltip() != '' else f"<p style='white-space:pre'> Parameter: <B>{self.name()}<B></p>"
        self.setToolTip(tooltip_string)
        self.setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")


    #TODO: Fix this. Would like to remove this func.
    @abstractmethod
    def bLabel(self) -> bool:
        return True


    @abstractmethod
    def eval(self) -> int or float or str:
        """ Gets parameter value."""

    @abstractmethod
    def set_value(self, value):
        """ set value for parameter """




class ParmSetup(WidgetSetup):

    def __init__(self,parent):
        super(ParmSetup, self).__init__(parent)
        pass
        
    @UIProperty(metaWidget='CheckProperty', label='Horizontal join',category= 'Setting')
    def bNeighbor(self):
        pass

    @abstractmethod
    def set_value(self, value):
        """ set value for parameter """





class FolderSetup(WidgetSetup):

    def __init__(self,parent):
        super(FolderSetup, self).__init__(parent)
        self._folder_layout = QtWidgets.QVBoxLayout()
        self._folder_layout.setSpacing(0)
        self._folder_layout.setContentsMargins(0, 0, 0, 0)
        self._folder_widget = None

        self._childWidgets = TemplateDataClass.TemplateGroup()

    @UIProperty(metaWidget='LineEditProperty',label='Tab Hidden When', category='Expressions')
    def tab_hide(self):
        pass

    @UIProperty(metaWidget='LineEditProperty', label='Tab Disable When', category='Expressions')
    def tab_disable(self):
        pass

    @UIProperty(metaWidget='LineEditProperty', label='Default', category='Setting')
    def default_value(self):
        pass

    @abstractmethod
    def clearLayout(self):
        pass

    @abstractmethod
    def set_value(self, value):
        """ set value for parameter """

    @abstractmethod
    def setTabHidden(self, state: bool):
        """ Implementation for hiding tab group """

    @abstractmethod
    def setTabDisable(self, state: bool):
        """ Implementation for disabling tab group """

    def PostUpdate(self):
        pass

    def templateGroup(self):
        return self._childWidgets

    def bisFolderList(self):
        return False

    def bLabel(self) -> bool:
        return False


    def _close_tab_change(self, index):
        for widget in self._folder_widget.last_widget_removed.templateGroupData():
            self._parent.widget_layout().pop(widget)

        for index in range(0,self._folder_widget.count()):
            widget_template = self._folder_widget.tabWidget.widget(index)
            for key in widget_template.templateGroupData():
                widget = self._parent.widget_layout()[key]
                del self._parent.widget_layout()[key]
                widget.__property_instances__['name'].setValue(widget.__property_instances__['name'].value()[:-1] + str(index + 1))
                widget._updateProperties()

                self._parent.widget_layout()[f'{widget.name()}'] = widget

                if widget._label_widget:
                    widget.setToolTip(f"<p style='white-space:pre'> Parameter: <B>{widget.name()}<B></p> {widget.tooltip()} " if widget.tooltip() != '' else f"<p style='white-space:pre'> Parameter: <B>{widget.name()}<B></p>")
                    widget.setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")

                    widget._label_widget.setToolTip(f"<p style='white-space:pre'> Parameter: <B>{widget.name()}<B></p> {widget.tooltip()} " if widget.tooltip() != '' else f"<p style='white-space:pre'> Parameter: <B>{widget.name()}<B></p>")
                    widget._label_widget.setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")


        self.notify_expressions()






