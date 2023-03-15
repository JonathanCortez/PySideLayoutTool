from PySideLayoutTool.UIEditorLib.UIEditorProperty import  UICProperty, PropertyFactory, IWidgetProperties
from . import DictionaryWidgetClass

@PropertyFactory.register('DictionaryProperty')
class DictionaryProperty(IWidgetProperties):

    def __init__(self):
        super(DictionaryProperty, self).__init__()
        self._keys = []
        self._values = []
        self._dict_widget = DictionaryWidgetClass.DictWidgetClass()
        self._layout.addWidget(self._dict_widget)

        self._dict_widget.table_widget.cellChanged.connect(self.updateValues)

    def override_default(self, defaults: tuple):
        pass

    def setValue(self, value):
        if len(value) == 2:
            for i in enumerate(value[0]):
                if i[0]+1 > self._dict_widget.count():
                    self._dict_widget.addDict()
                self._dict_widget.setkeyText(i[0],i[1])

            for i in enumerate(value[1]):
                if i[0]+1 > self._dict_widget.count():
                    self._dict_widget.addDict()
                self._dict_widget.setvalueText(i[0],i[1])
        else:
            for i in enumerate(value[0]):
                if i[0]+1 > self._dict_widget.count():
                    self._dict_widget.addDict()
                self._dict_widget.setkeyText(i[0],i[1])
                self._dict_widget.setvalueText(i[0],str(i[0]))


    def value(self):
        return list(self._keys), list(self._values)

    def updateValues(self):
        self._keys = self._dict_widget.DictionaryKeys()
        self._values = self._dict_widget.DictionaryValues()

    @UICProperty
    def keys(self):
        return self._keys

    @UICProperty
    def values(self):
        return self._values

