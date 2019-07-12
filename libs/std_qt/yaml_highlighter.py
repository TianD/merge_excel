# coding=utf8
# Copyright (c) 2018 CineUse

from Qt.QtCore import QRegExp, Qt
from Qt.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat


class YamlHighlighter(QSyntaxHighlighter):

    def __init__(self, parent=None):
        QSyntaxHighlighter.__init__(self, parent)
        self.rules = []
        self.commentStart = QRegExp("#")
        self.commentEnd = QRegExp("\n|\r")
        self.default_format = QTextCharFormat()
        self.default_format.setForeground(QColor(24, 24, 24))
        self.commentFormat = QTextCharFormat()
        self.commentFormat.setFontItalic(True)
        self.commentFormat.setForeground(Qt.darkGray)

        tag_list = ["\\btrue\\b", "\\bfalse\\b"]
        # create patterns for tags
        for tag in tag_list:
            self.rules.append((self._create_regexp(tag), self._create_format(Qt.blue)))

        # for default values
        self.rules.append((self._create_regexp("\w.*\w"), self._create_format(Qt.blue)))

        # for digits
        self.rules.append((self._create_regexp("\\d+"), self._create_format(QColor(127, 64, 127))))

        # for params
        self.rules.append((self._create_regexp("^\s*[_.\w]*\s*:"), self._create_format(Qt.green)))

        # for params
        self.rules.append((self._create_regexp("^\s*- [_.\w]*\s*:"), self._create_format(Qt.green)))

        # for params
        self.rules.append((self._create_regexp(":\s*:[_\.\w]*$|:\s*\@[_\.\w]*$"), self._create_format(Qt.green)))

        # for list signs
        self.rules.append((self._create_regexp("^\s*-"), self._create_format(Qt.darkRed, 'bold')))

        # for ???
        self.rules.append((self._create_regexp("^---$"), self._create_format(Qt.darkRed)))

        # for braces
        self.rules.append((self._create_regexp("[\[\]\{\}\,]"), self._create_format(Qt.darkGreen)))

        # create patterns for strings
        self.rules.append((self._create_regexp("\".*\"|\'.*\'"), self._create_format(Qt.blue)))

        # create patterns for substitutions
        self.rules.append((self._create_regexp("\\$\\(.*\\)"), self._create_format(QColor(127, 64, 127))))

        # create patterns for DOCTYPE
        self.rules.append((self._create_regexp("<!DOCTYPE.*>"), self._create_format(Qt.lightGray)))
        self.rules.append((self._create_regexp("<\\?xml.*\\?>"), self._create_format(Qt.lightGray)))

    def highlightBlock(self, text):
        self.setFormat(0, len(text), self.default_format)
        for pattern, form in self.rules:
            index = pattern.indexIn(text)
            while index >= 0:
                length = pattern.matchedLength()
                self.setFormat(index, length, form)
                index = pattern.indexIn(text, index + length)

        # mark comment blocks
        self.setCurrentBlockState(0)
        if self.previousBlockState() != 1:
            start_index = self.commentStart.indexIn(text)
            if start_index >= 0:
                comment_len = len(text) - start_index
                self.setFormat(start_index, comment_len, self.commentFormat)

    @staticmethod
    def _create_regexp(pattern=''):
        _regexp = QRegExp()
        _regexp.setMinimal(True)
        _regexp.setPattern(pattern)
        return _regexp

    @staticmethod
    def _create_format(color, style=''):
        _format = QTextCharFormat()
        _format.setForeground(color)
        if 'bold' in style:
            _format.setFontWeight(QFont.Bold)
        else:
            _format.setFontWeight(QFont.Normal)
        if 'italic' in style:
            _format.setFontItalic(True)
        return _format


if __name__ == "__main__":
    from Qt import QtWidgets
    app = QtWidgets.QApplication([])
    te = QtWidgets.QTextEdit()
    YamlHighlighter(te.document())
    te.show()
    app.exec_()

