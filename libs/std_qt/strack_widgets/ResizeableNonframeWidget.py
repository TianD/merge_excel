# coding:utf-8

import sys

sys.path.append(r"D:\repos\strack_desktop\pyLibs")

import sys
from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets

PADDING = 4
sys.setrecursionlimit(10000)


class ResizeableNonframeWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ResizeableNonframeWidget, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)
        self.SHADOW_WIDTH = 0  # 边框距离
        self.isLeftPressDown = False  # 鼠标左键是否按下
        self.dragPosition = 0  # 拖动时坐标
        self.Numbers = self.enum(UP=0, DOWN=1, LEFT=2, RIGHT=3, LEFTTOP=4, LEFTBOTTOM=5, RIGHTBOTTOM=6, RIGHTTOP=7,
                                 NONE=8)  # 枚举参数
        self.dir = self.Numbers.NONE  # 初始鼠标状态
        self.setMouseTracking(True)

    # 枚举参数
    def enum(self, **enums):
        return type('Enum', (), enums)

    def region(self, cursorGlobalPoint):
        # 获取窗体在屏幕上的位置区域，tl为topleft点，rb为rightbottom点
        rect = self.rect()
        tl = self.mapToGlobal(rect.topLeft())
        rb = self.mapToGlobal(rect.bottomRight())

        x = cursorGlobalPoint.x()
        y = cursorGlobalPoint.y()

        if (tl.x() + PADDING >= x and tl.x() <= x and tl.y() + PADDING >= y and tl.y() <= y):
            # 左上角
            self.dir = self.Numbers.LEFTTOP
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))  # 设置鼠标形状
        elif (x >= rb.x() - PADDING and x <= rb.x() and y >= rb.y() - PADDING and y <= rb.y()):
            # 右下角
            self.dir = self.Numbers.RIGHTBOTTOM
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))
        elif (x <= tl.x() + PADDING and x >= tl.x() and y >= rb.y() - PADDING and y <= rb.y()):
            # 左下角
            self.dir = self.Numbers.LEFTBOTTOM
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeBDiagCursor))
        elif (x <= rb.x() and x >= rb.x() - PADDING and y >= tl.y() and y <= tl.y() + PADDING):
            # 右上角
            self.dir = self.Numbers.RIGHTTOP
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeBDiagCursor))
        elif (x <= tl.x() + PADDING and x >= tl.x()):
            # 左边
            self.dir = self.Numbers.LEFT
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        elif (x <= rb.x() and x >= rb.x() - PADDING):
            # 右边
            self.dir = self.Numbers.RIGHT
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        elif (y >= tl.y() and y <= tl.y() + PADDING):
            # 上边
            self.dir = self.Numbers.UP
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        elif (y <= rb.y() and y >= rb.y() - PADDING):
            # 下边
            self.dir = self.Numbers.DOWN
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        else:
            # 默认
            self.dir = self.Numbers.NONE
            self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def mouseReleaseEvent(self, event):
        # 确定大小
        if (event.button() == QtCore.Qt.LeftButton):
            self.isLeftPressDown = False
            if (self.dir != self.Numbers.NONE):
                self.releaseMouse()
                self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def mousePressEvent(self, event):
        if (event.button() == QtCore.Qt.LeftButton):
            self.isLeftPressDown = True
            if (self.dir != self.Numbers.NONE):
                self.mouseGrabber()
            else:
                self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        # 改大小
        gloPoint = event.globalPos()
        rect = self.rect()
        tl = self.mapToGlobal(rect.topLeft())
        rb = self.mapToGlobal(rect.bottomRight())

        if (not self.isLeftPressDown):
            self.region(gloPoint)
        else:
            if (self.dir != self.Numbers.NONE):
                rmove = QtCore.QRect(tl, rb)
                if (self.dir == self.Numbers.LEFT):
                    if (rb.x() - gloPoint.x() <= self.minimumWidth()):
                        rmove.setX(tl.x())
                    else:
                        rmove.setX(gloPoint.x())
                elif (self.dir == self.Numbers.RIGHT):
                    rmove.setWidth(gloPoint.x() - tl.x())
                elif (self.dir == self.Numbers.UP):
                    if (rb.y() - gloPoint.y() <= self.minimumHeight()):
                        rmove.setY(tl.y())
                    else:
                        rmove.setY(gloPoint.y())
                elif (self.dir == self.Numbers.DOWN):
                    rmove.setHeight(gloPoint.y() - tl.y())
                elif (self.dir == self.Numbers.LEFTTOP):
                    if (rb.x() - gloPoint.x() <= self.minimumWidth()):
                        rmove.setX(tl.x())
                    else:
                        rmove.setX(gloPoint.x())
                    if (rb.y() - gloPoint.y() <= self.minimumHeight()):
                        rmove.setY(tl.y())
                    else:
                        rmove.setY(gloPoint.y())
                elif (self.dir == self.Numbers.RIGHTTOP):
                    rmove.setWidth(gloPoint.x() - tl.x())
                    rmove.setY(gloPoint.y())
                elif (self.dir == self.Numbers.LEFTBOTTOM):
                    rmove.setX(gloPoint.x())
                    rmove.setHeight(gloPoint.y() - tl.y())
                elif (self.dir == self.Numbers.RIGHTBOTTOM):
                    rmove.setWidth(gloPoint.x() - tl.x())
                    rmove.setHeight(gloPoint.y() - tl.y())
                else:
                    pass
                self.setGeometry(rmove)
                event.accept()


if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    wgt = ResizeableNonframeWidget()
    wgt.show()
    app.exec_()
