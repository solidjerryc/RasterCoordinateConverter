# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 15:47:10 2019

@author: JerryC
"""

from osgeo import gdal, osr
import coord_converter
import sys

def getSRSPair(dataset):
    '''
    获得给定数据的投影参考系和地理参考系
    :param dataset: GDAL地理数据
    :return: 投影参考系和地理参考系
    '''
    prosrs = osr.SpatialReference()
    prosrs.ImportFromWkt(dataset.GetProjection())
    geosrs = prosrs.CloneGeogCS()
    return prosrs, geosrs

def geo2lonlat(dataset, x, y):
    '''
    将投影坐标转为经纬度坐标（具体的投影坐标系由给定数据确定）
    :param dataset: GDAL地理数据
    :param x: 投影坐标x
    :param y: 投影坐标y
    :return: 投影坐标(x, y)对应的经纬度坐标(lon, lat)
    '''
    prosrs, geosrs = getSRSPair(dataset)
    ct = osr.CoordinateTransformation(prosrs, geosrs)
    coords = ct.TransformPoint(x, y)
    return coords[:2]

def lonlat2geo(dataset, lon, lat):
    '''
    将经纬度坐标转为投影坐标（具体的投影坐标系由给定数据确定）
    :param dataset: GDAL地理数据
    :param lon: 地理坐标lon经度
    :param lat: 地理坐标lat纬度
    :return: 经纬度坐标(lon, lat)对应的投影坐标
    '''
    prosrs, geosrs = getSRSPair(dataset)
    ct = osr.CoordinateTransformation(geosrs, prosrs)
    coords = ct.TransformPoint(lon, lat)
    return coords[:2]

def main(originPath, outPath):
    '''
    将原始文件转换为WGS84坐标
    : originPath 原始文件路径
    : outPath 转换后文件的输出路径
    '''
    dt=gdal.Open(originPath)

    Transform=dt.GetGeoTransform()
    b=geo2lonlat(dt, Transform[0], Transform[3])
    c=coord_converter.gcj02_to_wgs84(b[0],b[1])
    c_o=lonlat2geo(dt,c[0],c[1])

    driver = gdal.GetDriverByName('GTiff')
    rasterCount=dt.RasterCount
    outRaster = driver.Create(outPath, dt.RasterXSize, dt.RasterYSize, rasterCount, dt.GetRasterBand(1).DataType)
    outRaster.SetGeoTransform((c_o[0], Transform[1],Transform[2],c_o[1],Transform[4],Transform[5]))
    for i in range(rasterCount):
        outband = outRaster.GetRasterBand(i+1)
        outband.WriteArray(dt.ReadAsArray()[i])

    outRaster.SetProjection(dt.GetProjection())
    outRaster.FlushCache()
    del outRaster
    
if __name__=='__main__':
    '''
    命令行输入参数，如不需要可以直接调用main函数
    '''
    if len(sys.argv)==1:
        print('Please input file path.')
    elif len(sys.argv)==2:
        originPath=sys.argv[1]
        outPath=sys.argv[1].split('.tif')[0]+'_new.tif'
        main(originPath, outPath)
    elif len(sys.argv)==3:
        originPath=sys.argv[1]
        outPath=sys.argv[2]
        main(originPath, outPath)
    else:
        print('Input error!')

    

