# -*- coding: utf-8 -*-
def classFactory(iface):
    from .bufferfeatures import BufferFeatures
    return BufferFeatures(iface)
