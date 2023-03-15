from PySideLayoutTool.UIEditorLib.UIEditorProperty import  UICProperty, PropertyFactory, IWidgetProperties
from . import ComboBoxWidgetClass

@PropertyFactory.register('ComboProperty')
class ComboBoxProperty(IWidgetProperties):

    def __init__(self):
        super(ComboBoxProperty, self).__init__()
        self._current_item_name = None
        self._current_item_index = -1
        self._combo_widget = ComboBoxWidgetClass.ComboBoxWidget()
        self._layout.addWidget(self._combo_widget)
        self._items = None

        self._combo_widget._combo_box.activated.connect(self._comboChanged)

    def override_default(self, defaults: tuple):
        self.setItems(defaults)
        self._current_item_index = self.currentItemIndex()
        self._current_item_name = self._combo_widget._combo_box.currentText()

    def setValue(self, value):
        self.setItems(value['general_values'])
        self.setCurrentItem(value['current_value'])
        self._current_item_name = value['current_value']
        self._current_item_index = self.currentItemIndex()

    def value(self):
        return {'current_value': self._combo_widget._combo_box.currentText(), 'general_values': self._items}

    def setCurrentItem(self, text):
        self._combo_widget._combo_box.setCurrentText(text)
        self._current_item_name = self._combo_widget._combo_box.currentText()
        self._current_item_index = self.currentItemIndex()

    def setItems(self, items):
        self._items = items
        self._combo_widget._combo_box.addItems(items)

    def _comboChanged(self, arg__1):
        self._current_item_name = self._combo_widget._combo_box.currentText()
        self._current_item_index = self.currentItemIndex()

    def propertyWidget(self):
        return self._combo_widget._combo_box

    def currentItemIndex(self):
        return self._combo_widget._combo_box.currentIndex()

    @UICProperty
    def currentItem_name(self):
        return self._current_item_name

    @UICProperty
    def currentItem_index(self):
        return self._current_item_index