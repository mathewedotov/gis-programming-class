# -*- coding: utf-8 -*-
import os
from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtWidgets import QAction, QMessageBox
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsVectorLayer, QgsFeature, QgsProject

class BufferFeatures(QObject):
    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.action = None

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')
        self.action = QAction(QIcon(icon_path), "Buffer Features", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        layer = self.iface.activeLayer()
        if not layer or layer.type() != layer.VectorLayer:
            QMessageBox.information(self.iface.mainWindow(), "Buffer Features", "Выберите активный векторный слой.")
            return
        new_layer = QgsVectorLayer(f"Polygon?crs={layer.crs().authid()}", layer.name() + "_buffer", "memory")
        provider = new_layer.dataProvider()
        for feat in layer.getFeatures():
            buffer_geom = feat.geometry().buffer(100, 8)
            new_feat = QgsFeature()
            new_feat.setGeometry(buffer_geom)
            provider.addFeatures([new_feat])
        new_layer.updateExtents()
        QgsProject.instance().addMapLayer(new_layer)
        QMessageBox.information(self.iface.mainWindow(), "Buffer Features", "Буфер создан и добавлен на карту.")
