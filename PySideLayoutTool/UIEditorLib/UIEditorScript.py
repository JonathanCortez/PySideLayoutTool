from PySide2 import QtGui, QtCore, QtWidgets
from typing import Dict, List, Any


class ScriptEditor(QtWidgets.QPlainTextEdit):

    def __init__(self):
        super(ScriptEditor, self).__init__()
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
                super(ScriptEditor, self).keyPressEvent(event)
        else:
            super(ScriptEditor, self).keyPressEvent(event)


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