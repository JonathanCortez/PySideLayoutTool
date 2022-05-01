from typing import Dict, List, Any
from PySide2 import QtWidgets, QtCore, QtGui

from PySideLayoutTool.UIEditorLib import UIEditorIconFactory


class ScriptTab(QtWidgets.QMainWindow):

    def __init__(self, parent):
        super(ScriptTab, self).__init__()
        self._parent = parent
        self._editor_dock = QtWidgets.QDockWidget(self)
        self._editor_dock.setWindowTitle('Python Editor')
        self._editor_dock.setAllowedAreas(QtCore.Qt.TopDockWidgetArea)

        self._editor_layout = EditorLayout()
        self._editor_dock.setWidget(self._editor_layout)
        self._editor_dock.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable | QtWidgets.QDockWidget.DockWidgetMovable)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea,self._editor_dock)

    def getPyModules(self):
        return self._editor_layout

    def pyModules_count(self):
        return self._editor_layout.module_count()

    def pyModule_editor(self):
        return self._editor_layout


class EditorLayout(QtWidgets.QWidget):

    def __init__(self):
        super(EditorLayout, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0,0,0,0)

        self._top_toolbar = QtWidgets.QToolBar()
        self._bottom_toolbar = QtWidgets.QToolBar()
        self._pyModules = {}

        self._left_move_action = self._top_toolbar.addAction(UIEditorIconFactory.IconEditorFactory.create('move_left'), 'Line Left Move')
        self._right_move_action = self._top_toolbar.addAction(UIEditorIconFactory.IconEditorFactory.create('move_right'), 'Line Right Move')

        self._top_toolbar.addSeparator()

        self._comment_action = self._top_toolbar.addAction(UIEditorIconFactory.IconEditorFactory.create('comment'), 'Comment In/Out')
        self._top_toolbar.addSeparator()

        spacing = QtWidgets.QWidget()
        spacing.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        spacing.setStyleSheet('background-color: #0e0e0e;')

        self._bottom_toolbar.addWidget(spacing)
        self._bottom_toolbar.addSeparator()
        self._zoom_in_action = self._bottom_toolbar.addAction(UIEditorIconFactory.IconEditorFactory.create('zoom_In'), 'Increase Text Size')
        self._zoom_out_action = self._bottom_toolbar.addAction(UIEditorIconFactory.IconEditorFactory.create('zoom_Out'), 'Decrease Text Size')

        self._tab_widget = QtWidgets.QTabWidget(self)
        self._tab_widget.setProperty('class','editor_pane')
        self._tab_widget.setTabsClosable(True)

        self._base_pyModule = CodeEditor()
        self._tab_widget.addTab(self._base_pyModule,'PyModule_1')
        self._tab_widget.tabBar().tabButton(0,QtWidgets.QTabBar.RightSide).resize(0, 0)
        self._pyModules['PyModule_1'] = self._base_pyModule

        self._tab_widget.addTab(QtWidgets.QWidget(), '+' )
        self._tab_widget.tabBar().tabButton(1, QtWidgets.QTabBar.RightSide).resize(0, 0)

        self._tab_widget.tabBar().setSelectionBehaviorOnRemove(QtWidgets.QTabBar.SelectLeftTab)

        self._layout.addWidget(self._top_toolbar)
        self._layout.addWidget(self._tab_widget)
        self._layout.addWidget(self._bottom_toolbar)

        self._left_move_action.triggered.connect(self.move_line_back)
        self._right_move_action.triggered.connect(self.move_line_forward)
        self._comment_action.triggered.connect(self.comment_action)

        self._zoom_in_action.triggered.connect(self.zoom_in_call)
        self._zoom_out_action.triggered.connect(self.zoom_out_call)

        self._tab_widget.tabBarClicked.connect(self.newTab)
        self._tab_widget.tabBar().tabCloseRequested.connect(self.closeTab)

        self.setLayout(self._layout)

    def scriptModule(self, name):
        if name in self._pyModules:
            return self._pyModules[name]

    def module_count(self) -> int:
        return len(self._pyModules)

    def modules(self):
        return self._pyModules

    def newTab(self, index):
        if self._tab_widget.tabText(index) == "+":
            new_pyModule = CodeEditor()
            self._tab_widget.insertTab(index, new_pyModule, f'PyModule_{index+1}')
            self._pyModules[f'PyModule_{index+1}'] = new_pyModule

    def newTabCode(self,index, name, code):
        if name not in self._pyModules:
            new_pyModule = CodeEditor()
            new_pyModule.appendPlainText(code)
            self._tab_widget.insertTab(index, new_pyModule, name)
            self._pyModules[name] = new_pyModule

        else:
            self._pyModules[name].appendPlainText(code)

    def closeTab(self, index):
        widget = self._tab_widget.widget(index)
        text = self._tab_widget.tabText(index)
        self._tab_widget.removeTab(index)
        editor_class = self._pyModules.pop(text)
        del widget, editor_class

    def move_line_back(self, state):
        widget = self._tab_widget.widget(self._tab_widget.currentIndex())
        widget.reverse_TabHandling()

    def move_line_forward(self, state):
        widget = self._tab_widget.widget(self._tab_widget.currentIndex())
        widget.tab_effect()

    def comment_action(self, state):
        widget = self._tab_widget.widget(self._tab_widget.currentIndex())
        widget.commentHandling()

    def zoom_in_call(self, state):
        widget = self._tab_widget.widget(self._tab_widget.currentIndex())
        widget.zoom_in()

    def zoom_out_call(self, state):
        widget = self._tab_widget.widget(self._tab_widget.currentIndex())
        widget.zoom_out()


#TODO: On insert new tab with CodeEditor seems to crash Window.
#       Find why CodeEditor class is being deleted early.

class CodeEditor(QtWidgets.QPlainTextEdit):

    def __init__(self):
        super(CodeEditor, self).__init__()
        self._lineNumberArea = LineNumberArea(self)
        self._block_count = 1
        self._highlighter = EditorHighlighter(self.document())

        self._backtab_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence('Shift+Tab'), self)
        self._backtab_shortcut.activated.connect(self.reverse_TabHandling)

        self._comment_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+/'), self)
        self._comment_shortcut.activated.connect(self.commentHandling)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.setTabStopDistance(QtGui.QFontMetricsF(self.font()).horizontalAdvance(' ') * 5)
        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()


    def zoom_in(self):
        self.zoomIn(1)

    def zoom_out(self):
        self.zoomOut(1)


    def keyPressEvent(self, event) -> None:
        if event.key() == QtCore.Qt.Key_Tab:
            cursor = self.textCursor()
            if cursor.hasSelection():
                sum = self.multiLine(cursor)

                if sum > 0:
                    for i in range(0, sum + 1):
                        cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                        cursor = self.firstChar(cursor)
                        cursor.insertText('\t')
                        cursor.movePosition(QtGui.QTextCursor.NextBlock)
                else:
                    self.tab_effect()

                cursor.clearSelection()
                self.setTextCursor(cursor)
            else:
                super(CodeEditor, self).keyPressEvent(event)
        else:
            super(CodeEditor, self).keyPressEvent(event)


    def tab_effect(self):
        cursor = self.textCursor()
        cursor.movePosition(QtGui.QTextCursor.StartOfLine)
        cursor.insertText('\t')
        cursor.movePosition(QtGui.QTextCursor.NextWord)
        self.setTextCursor(cursor)


    def reverse_TabHandling(self):
        cursor = self.textCursor()
        if cursor.hasSelection():
            sum = self.multiLine(cursor)

            if sum > 0:
                for i in range(0, sum ):
                    cursor = self.reverseTab(cursor)
                    cursor.movePosition(QtGui.QTextCursor.NextBlock)

            else:
                cursor = self.reverseTab(cursor)
        else:
            cursor = self.reverseTab(cursor)

        cursor.clearSelection()
        self.setTextCursor(cursor)


    def reverseTab(self, cursor):
        cursor.movePosition(QtGui.QTextCursor.StartOfLine)
        cursor.movePosition(QtGui.QTextCursor.NextWord, QtGui.QTextCursor.KeepAnchor)
        sel_text = cursor.selectedText()

        if sel_text.startswith('\t'):
            text = sel_text.replace('\t', '', 1)
            cursor.insertText(text)

        return cursor


    def multiLine(self, cursor):
        start_pos = cursor.selectionStart()
        end_pos = cursor.selectionEnd()

        start_block_index = self.document().findBlock(start_pos).blockNumber()
        end_block_index = self.document().findBlock(end_pos).blockNumber()

        cursor.setPosition(start_pos)
        sum = end_block_index - start_block_index
        return sum


    def commentHandling(self):
        cursor = self.textCursor()
        if cursor.hasSelection():
            sum = self.multiLine(cursor)
            if sum > 0:
                for i in range(0,sum+1):
                    cursor = self.commentInOut(cursor)
                    cursor.movePosition(QtGui.QTextCursor.NextBlock)
            else:
                cursor = self.commentInOut(cursor)

        else:
            cursor = self.commentInOut(cursor)

        cursor.clearSelection()
        self.setTextCursor(cursor)



    def commentInOut(self, cursor):
        cursor.movePosition(QtGui.QTextCursor.StartOfLine)
        cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor)
        sel_text = cursor.selectedText()

        if sel_text.startswith('\t'):
            cursor.clearSelection()
            cursor.movePosition(QtGui.QTextCursor.StartOfLine)
            cursor = self.firstChar(cursor)

        else:
            cursor.clearSelection()
            cursor.movePosition(QtGui.QTextCursor.Left)

        cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor)
        sel_text = cursor.selectedText()

        if sel_text.startswith('#'):
            cursor.deleteChar()
            cursor.deleteChar()
        else:
            cursor.clearSelection()
            cursor.movePosition(QtGui.QTextCursor.Left)
            cursor.insertText('# ')

        return cursor



    def firstChar(self, cursor):
        cursor.movePosition(QtGui.QTextCursor.NextWord)
        sel_text = cursor.selectedText()

        if sel_text.startswith('\t'):
            cursor = self.firstChar(cursor)

        return cursor



    def lineNumberAreaPaintEvent(self, event):
        painter = QtGui.QPainter(self._lineNumberArea)
        painter.fillRect(event.rect(),QtCore.Qt.darkGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(QtCore.Qt.black)
                painter.drawText(0, top, self._lineNumberArea.width() - 2, self.fontMetrics().height(),QtCore.Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            blockNumber += 1


    def lineNumberAreaWidth(self) -> int:
        digits = 1
        maxCount = max(1, self.blockCount())
        while maxCount >= 10:
            maxCount /= 10
            digits += 1

        space = 5 + self.fontMetrics().horizontalAdvance('9',1) * digits
        return space


    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)

        cr = self.contentsRect()
        self._lineNumberArea.setGeometry(QtCore.QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))



    def updateLineNumberAreaWidth(self, newBlockCount: int) -> None:
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

        if self._block_count < newBlockCount:
            text_doc = self.document()
            text_block = text_doc.findBlockByLineNumber(newBlockCount-2)

            for rule in self._highlighter.highlightingRules['keywords']:
                expression = QtCore.QRegExp(rule.pattern)
                start_index = expression.indexIn( text_block.text() )
                keyword = True if expression.capturedTexts()[0] in ['class', 'def', 'if','elif','else'] else False
                if start_index >= 0 and keyword:
                    self.insertPlainText('\t')
                    break

            self._block_count += 1
        else:
            self._block_count -= 1



    def highlightCurrentLine(self) -> None:
        pass
        # extraSelections = self.extraSelections()
        #
        # if not self.isReadOnly():
        #     selection = QtWidgets.QTextEdit.ExtraSelection()
        #     lineColor = QtGui.QColor('#2f2f2f').lighter(150)
        #
        #     selection.format.setBackground(lineColor)
        #     selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
        #     selection.cursor = self.textCursor()
        #     selection.cursor.clearSelection()
        #     extraSelections.append(selection)
        #
        # self.setExtraSelections(extraSelections)


    def updateLineNumberArea(self, rect: QtCore.QRect, dy: int):
        self._rect = QtCore.QRect(0,rect.y(), self._lineNumberArea.width(), rect.height())
        if dy:
            self._lineNumberArea.scroll(0, dy)
        else:
            self._lineNumberArea.update(0, rect.y(), self._lineNumberArea.width(), rect.height())

        # if rect.contains(self.viewport().rect()):
        #     self.updateLineNumberAreaWidth(0)



class LineNumberArea(QtWidgets.QWidget):

    def __init__(self, parent_editor):
        super(LineNumberArea, self).__init__(parent_editor)
        self._editor_parent = parent_editor

    def sizeHint(self):
        return QtCore.Qt.QSize(self._editor_parent.lineNumberAreaWidth(), 0)

    def paintEvent(self, event) -> None:
        self._editor_parent.lineNumberAreaPaintEvent(event)


class EditorHighlighter(QtGui.QSyntaxHighlighter):

    def __init__(self, parent):
        super(EditorHighlighter, self).__init__(parent)
        keyword = QtGui.QTextCharFormat()
        reservedClasses = QtGui.QTextCharFormat()
        assignmentOperator = QtGui.QTextCharFormat()
        delimiter = QtGui.QTextCharFormat()
        dunderClasses = QtGui.QTextCharFormat()
        selfassignmentOperator = QtGui.QTextCharFormat()
        number = QtGui.QTextCharFormat()
        comment = QtGui.QTextCharFormat()
        string = QtGui.QTextCharFormat()
        singleQuotedString = QtGui.QTextCharFormat()

        self.highlightingRules: Dict[str, List[Any]] = {}

        # keyword
        brush = QtGui.QBrush(QtGui.QColor('#ffa000'))
        keyword.setForeground(brush)
        keywords = ["break", "else", "for", "if", "in","elif",
                    "or", "yield", "return", "pass","None",
                    "try", "while","and", "class", "def",
                    "True", "False", "None","import", "from"]
        rule_list = []
        for word in keywords:
            pattern = QtCore.QRegExp("\\b" + word + "\\b")
            rule = HighlightingRule(pattern, keyword)
            rule_list.append(rule)
            self.highlightingRules['keywords'] = rule_list

        # reservedClasses
        brush = QtGui.QBrush(QtGui.QColor('#c067ff'))
        reservedClasses.setForeground(brush)
        keywords = ["abs", "aiter", "all","any","anext","ascii",
                    "bin", "bool", "breakpoint","bytearray", "bytes",
                    "callable", "chr", "classmethod","compile", "complex",
                    "delattr", "dict", "dir", "divmod", "enumerate", "eval",
                    "exec", "filter", "float", "format", "forzenset", "getattr",
                    "globals", "hasattr", "hash", "help", "hex", "id", "input",
                    "int", "isinstance", "issubclass","iter","len", "list","locals",
                    "map", "max","min","memoryview", "next", "object", "oct", "open",
                    "ord", "pow", "print", "property", "range","repr", "reversed",
                    "round", "set", "setattr", "slice","sorted","staticmethod","str",
                    "sum", "super", "tuple", "type", "vars","zip", "__import__"]

        rule_list = []
        for word in keywords:
            pattern = QtCore.QRegExp("\\b" + word + "\\b")
            rule = HighlightingRule(pattern, reservedClasses)
            rule_list.append(rule)
            self.highlightingRules['reserved_Classes'] = rule_list


        brush = QtGui.QBrush(QtGui.QColor('#eda1fe'))
        pattern = QtCore.QRegExp("self")
        selfassignmentOperator.setForeground(brush)
        rule = HighlightingRule(pattern, selfassignmentOperator)
        self.highlightingRules['self_assignment'] = [rule]

        brush = QtGui.QBrush(QtGui.QColor('#c7068d'))
        pattern = QtCore.QRegExp("[_]{2,2}\w+")
        dunderClasses.setForeground(brush)
        rule = HighlightingRule(pattern, dunderClasses)
        self.highlightingRules['dunder_Classes'] = [rule]

        # assignmentOperator
        brush = QtGui.QBrush(QtGui.QColor('#5f81ff'))
        pattern = QtCore.QRegExp("(<){1,2}-")
        assignmentOperator.setForeground(brush)
        # assignmentOperator.setFontWeight(QtGui.QFont.Bold)
        rule = HighlightingRule(pattern, assignmentOperator)
        self.highlightingRules['assignmentOperator'] = [rule]

        # number
        pattern = QtCore.QRegExp("[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?")
        pattern.setMinimal(True)
        number.setForeground(brush)
        rule = HighlightingRule(pattern, number)
        self.highlightingRules['numbers'] = [rule]

        # comment
        brush = QtGui.QBrush(QtCore.Qt.darkGray ,QtCore.Qt.SolidPattern)
        pattern = QtCore.QRegExp("#.*")
        comment.setForeground(brush)
        rule = HighlightingRule(pattern, comment)
        self.highlightingRules['comments'] = [rule]

        # string
        brush = QtGui.QBrush(QtGui.QColor('#007a2b'))
        pattern = QtCore.QRegExp("\".*\"")
        pattern.setMinimal(True)
        string.setForeground(brush)
        rule = HighlightingRule(pattern, string)
        self.highlightingRules['strings'] = [rule]

        # singleQuotedString
        brush = QtGui.QBrush(brush)
        pattern = QtCore.QRegExp("\'.*\'")
        pattern.setMinimal(True)
        singleQuotedString.setForeground(brush)
        rule = HighlightingRule(pattern, singleQuotedString)
        self.highlightingRules['singleQuotedString'] = [rule]


    def highlightBlock( self, text ):
      for key in self.highlightingRules:
        for rule in self.highlightingRules[key]:
            expression = QtCore.QRegExp( rule.pattern )
            index = expression.indexIn( text )

            while index >= 0:
              length = expression.matchedLength()
              self.setFormat( index, length, rule.format )
              index = expression.indexIn(text, index + length)

        self.setCurrentBlockState( 0 )


class HighlightingRule():
  def __init__( self, pattern, format ):
    self.pattern = pattern
    self.format = format