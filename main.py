# -*- coding: utf-8 -*-
# @Author: Bardbo
# @Date:   2020-11-09 22:02:58
# @Last Modified by:   Bardbo
# @Last Modified time: 2020-11-09 22:04:34
from get_bus_line_station_data_by_gaode import *
from line_station_data_to_shp import *
import time

if __name__ == '__main__':
    # 此处参数需更改
    city = '益阳'
    city_phonetic = 'yiyang'
    ak = '5c97181290522e9fea1ff5d32208634f'  # 这里建议更改为自己的key

    start_time = time.time()
    print(f'==========正在获取 {city} 线路名称==========')
    line_names = get_bus_line_name(city_phonetic)
    print(f'{city}在公交网上显示共有{len(line_names)}条线路')
    for line_name in tqdm(line_names):
        get_line_station_data(city, line_name, ak, city_phonetic)
    end_time = time.time()
    print(f'我爬完啦, 耗时{end_time - start_time}秒')

    print('正在创建shp文件')
    dts = DataToShp(city_phonetic + '_lines.csv')
    dts.get_station_data()
    dts.get_line_data()
    dts.create_station_shp()
    dts.create_lines_shp()
    print('shp文件创建完成')
