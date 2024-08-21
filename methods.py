from PyQt5.QtGui import QTextCursor

import socket

def addValueToTable(text_editor, port, service, status="open"):
    text_editor.insertText(str(port))
    text_editor.movePosition(QTextCursor.NextCell)
    text_editor.insertText(status)
    text_editor.movePosition(QTextCursor.NextCell)
    text_editor.insertText(service)
    text_editor.movePosition(QTextCursor.NextCell)
    text_editor.movePosition(QTextCursor.NextCell)
