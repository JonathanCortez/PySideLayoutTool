from PySide2 import QtWidgets, QtCore


class DictWidgetClass(QtWidgets.QWidget):

    def __init__(self):
        super(DictWidgetClass, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.setAlignment(QtCore.Qt.AlignTop)

        self._dict_key_value = {}

        self.table_widget = QtWidgets.QTableWidget(1, 2)
        self.table_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self._table_size = 62
        self._table_height = 30

        hor_header = self.table_widget.horizontalHeader()
        hor_header.setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)
        hor_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        vert_header = self.table_widget.verticalHeader()
        vert_header.setProperty('class','side_HeaderView')
        vert_header.setSectionResizeMode(0,QtWidgets.QHeaderView.Fixed)

        self.table_widget.setMinimumHeight(self._table_size)
        self.table_widget.setMaximumHeight(self._table_size)

        self.table_widget.setHorizontalHeaderLabels(['Key', 'Value'])

        hor_layout = QtWidgets.QHBoxLayout()
        hor_layout.setSpacing(3)
        hor_layout.setContentsMargins(0,0,0,0)
        hor_layout.setAlignment(QtCore.Qt.AlignLeft)

        self.add_button = QtWidgets.QPushButton('+')
        self.add_button.setMinimumWidth(25)
        self.add_button.setMaximumWidth(25)
        self.add_button.setProperty('class', 'add_press')

        self.sub_button = QtWidgets.QPushButton('-')
        self.sub_button.setMinimumWidth(25)
        self.sub_button.setMaximumWidth(25)
        self.sub_button.setProperty('class', 'red_press')


        hor_layout.addWidget(self.add_button)
        hor_layout.addWidget(self.sub_button)

        self._layout.addWidget(self.table_widget)
        self._layout.addSpacing(2)
        self._layout.addLayout(hor_layout)

        self.setLayout(self._layout)

        self.add_button.clicked.connect(self.addDict)
        self.sub_button.clicked.connect(self.removeDict)

        self.table_widget.cellChanged.connect(self.cellText)

    def base_table_height(self):
        return self._table_height

    def count(self):
        return self.table_widget.rowCount()

    def addDict(self):
        count = self.table_widget.rowCount()
        self.table_widget.insertRow(count)

        if count < 5:
            self._table_size += self._table_height

        self.table_widget.setMinimumHeight(self._table_size)
        self.table_widget.setMaximumHeight(self._table_size)
        vert_header = self.table_widget.verticalHeader()
        vert_header.setSectionResizeMode(count, QtWidgets.QHeaderView.Fixed)

    def removeDict(self):
        count = self.table_widget.rowCount()
        if count > 1:
            self.table_widget.removeRow(count - 1)
            if count <= 5:
                self._table_size -= self._table_height

        self.table_widget.setMinimumHeight(self._table_size)
        self.table_widget.setMaximumHeight(self._table_size)
        self.table_widget.resize(self.table_widget.sizeHint().width(), self.table_widget.sizeHint().height())


    def setkeyText(self, row: int, text: str):
        item = self.table_widget.item(row, 0)
        if not item:
            self.table_widget.setItem(row,0,QtWidgets.QTableWidgetItem(text))
        else:
            item.setText(text)

    def setvalueText(self,row: int, text: str):
        item = self.table_widget.item(row, 1)
        if not item:
            self.table_widget.setItem(row,1,QtWidgets.QTableWidgetItem(text))
        else:
            item.setText(text)

    def DictionaryKeys(self):
        return self._dict_key_value.keys()

    def DictionaryValues(self):
        return self._dict_key_value.values()

    def cellText(self,row, column):
        current_item = self.table_widget.item(row, column)
        current_item_text = current_item.text()
        if column == 1:
            key_item = self.table_widget.item(row, 0)
            key_text = str(row)
            if key_item is not None:
                key_text = key_item.text()

            if key_text in self._dict_key_value or str(row) in self._dict_key_value:
                self._dict_key_value[key_text] = current_item_text
            else:
                self._dict_key_value[str(row)] = current_item_text
        else:
            value_item = self.table_widget.item(row, 0)
            if value_item is not None:
                value_text = value_item.text()
            else:
                value_text = ''
            self._dict_key_value[current_item_text] = value_text


    def sizeHint(self):
        return QtCore.QSize(400,self._table_size)