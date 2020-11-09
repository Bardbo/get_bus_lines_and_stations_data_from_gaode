# -*- coding: utf-8 -*-
# @Author: Bardbo
# @Date:   2020-11-09 21:09:12
# @Last Modified by:   Bardbo
# @Last Modified time: 2020-11-09 21:59:35
import pandas as pd
import numpy as np
import shapefile
import converter


class DataToShp:
    def __init__(self, filename):
        self.data = pd.read_csv(filename,
                                names=[
                                    'line_name', 'polyline', 'price',
                                    'station_names', 'station_coords'
                                ])

    def get_station_data(self):
        df_stations = self.data[['station_coords', 'station_names']]
        # 将原本的一行字符串变为列表
        df_stations['station_coords'] = df_stations['station_coords'].apply(
            lambda x: x.replace('[', '').replace(']', '').replace(
                '\'', '').split(', '))
        df_stations['station_names'] = df_stations['station_names'].apply(
            lambda x: x.replace('[', '').replace(']', '').replace(
                '\'', '').split(', '))
        # 横置的数据变为纵向的数据
        station_all = pd.DataFrame(\
                      np.column_stack((\
                                       np.hstack(df_stations['station_coords'].repeat(list(map(len, df_stations['station_coords'])))),
                                       np.hstack(df_stations['station_names'].repeat(list(map(len, df_stations['station_names']))))
                                     )),
                      columns=['station_coords','station_names'])
        # 去除重复
        station_all = station_all.drop_duplicates()
        # 坐标转换
        station_all['st_coords_wgs84'] = station_all['station_coords'].apply(
            self.stations_to_wgs84)
        station_all.reset_index(inplace=True)
        self.stations = station_all

    def get_line_data(self):
        df_lines = self.data[['line_name', 'polyline']]
        df_lines['polyline'] = df_lines['polyline'].apply(
            lambda x: x.split(';'))
        # 坐标转换
        df_lines['lines_wgs84'] = df_lines['polyline'].apply(
            self.lines_to_wgs84)
        df_lines.reset_index(inplace=True)
        self.lines = df_lines

    def stations_to_wgs84(self, coor):
        xy = coor.split(',')
        lng, lat = float(xy[0]), float(xy[1])
        return converter.gcj02_to_wgs84(lng, lat)

    def lines_to_wgs84(self, coor):
        ls = []
        for c in coor:
            xy = c.split(',')
            lng, lat = float(xy[0]), float(xy[1])
            ls.append(converter.gcj02_to_wgs84(lng, lat))
        return ls

    def create_station_shp(self):
        w = shapefile.Writer('./data/stations.shp')
        w.field('name', 'C')
        for i in range(len(self.stations)):
            w.point(self.stations['st_coords_wgs84'][i][0],
                    self.stations['st_coords_wgs84'][i][1])
            w.record(self.stations['station_names'][i])
        w.close()

    def create_lines_shp(self):
        w = shapefile.Writer('./data/lines.shp')
        w.field('name', 'C')
        for i in range(len(self.lines)):
            w.line([self.lines['lines_wgs84'][i]])
            w.record(self.lines['line_name'][i])
        w.close()


if __name__ == '__main__':
    dts = DataToShp('yiyang_lines.csv')
    dts.get_station_data()
    dts.get_line_data()
    dts.create_station_shp()
    dts.create_lines_shp()
    print('shp文件创建完成')
