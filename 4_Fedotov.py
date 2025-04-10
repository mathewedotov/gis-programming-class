from osgeo import gdal
from qgis.core import QgsVectorLayer, QgsProject
import numpy as np

# === ПУТИ К ФАЙЛАМ (Фёдоров, изображение №2) ===
input_raster_path = 'C:/QGIS_Project/no_crs/2.tif'
output_raster_path = 'C:/QGIS_Project/no_crs/2_fedotov_copy.tif'
footprint_path = 'C:/QGIS_Project/footprints/footprint_2.geojson'

# === ОТКРЫТИЕ ИСХОДНОГО РАСТРА ===
raster = gdal.Open(input_raster_path)
if raster is None:
    raise RuntimeError("Ошибка открытия растра")

width, height = raster.RasterXSize, raster.RasterYSize
print(f"Размер: {width} x {height}, каналов: {raster.RasterCount}")

# === ЧТЕНИЕ КАНАЛОВ ===
band_arrays = []
for idx in range(1, raster.RasterCount + 1):
    band = raster.GetRasterBand(idx)
    band_data = band.ReadAsArray().astype(np.float32)
    band_arrays.append(band_data)

# === СОЗДАНИЕ КОПИИ РАСТРА ===
driver = gdal.GetDriverByName('GTiff')
out_raster = driver.Create(output_raster_path, width, height, raster.RasterCount, gdal.GDT_Float32)

for i, data in enumerate(band_arrays):
    out_raster.GetRasterBand(i + 1).WriteArray(data)

# === ЗАГРУЗКА ВЕКТОРНОГО СЛОЯ ===
vector_layer = QgsVectorLayer(footprint_path, 'footprint', 'ogr')
if not vector_layer.isValid():
    raise Exception("Ошибка загрузки векторного слоя")

# === ИЗВЛЕЧЕНИЕ УГЛОВЫХ ТОЧЕК ===
feature = next(vector_layer.getFeatures())
polygon = feature.geometry().asPolygon()[0]
corner_coords = [(p.x(), p.y()) for p in polygon[:4]]

# === ЗАДАНИЕ ПРОЕКЦИИ ===
crs = vector_layer.crs()
out_raster.SetProjection(crs.authid())

# === СОЗДАНИЕ СПИСКА GCP ===
gcps = [
    gdal.GCP(corner_coords[0][0], corner_coords[0][1], 0, 0, 0),
    gdal.GCP(corner_coords[1][0], corner_coords[1][1], 0, width - 1, 0),
    gdal.GCP(corner_coords[2][0], corner_coords[2][1], 0, width - 1, height - 1),
    gdal.GCP(corner_coords[3][0], corner_coords[3][1], 0, 0, height - 1)
]

# === ПРИМЕНЕНИЕ ОПОРНЫХ ТОЧЕК ===
out_raster.SetGCPs(gcps, out_raster.GetProjection())
out_raster.FlushCache()

print("Скрипт Федотова (изображение 2) успешно выполнен.")
