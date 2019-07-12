# coding=utf8
# Copyright (c) 2018 CineUse

from Qt import QtGui
from Qt import QtCore


def create_round_image(image_path, wide=50):
    """
    Create a circle thumbnail

    :param image_path: QImage representing a thumbnail
    :returns: Round QPixmap
    """
    image = QtGui.QImage(image_path)

    # get the 512 base image
    base_image = QtGui.QPixmap(wide, wide)
    base_image.fill(QtCore.Qt.transparent)

    # now attempt to load the image
    # pixmap will be a null pixmap if load fails
    thumb = QtGui.QPixmap.fromImage(image)

    if not thumb.isNull():
        # scale it down to fit inside a frame of maximum 512x512
        thumb_scaled = thumb.scaled(wide,
                                    wide,
                                    QtCore.Qt.KeepAspectRatioByExpanding,
                                    QtCore.Qt.SmoothTransformation)

        # now composite the thumbnail on top of the base image
        # bottom align it to make it look nice
        thumb_img = thumb_scaled.toImage()
        brush = QtGui.QBrush(thumb_img)
        painter = QtGui.QPainter(base_image)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(brush)
        painter.drawEllipse(0, 0, wide, wide)
        painter.end()

    return base_image