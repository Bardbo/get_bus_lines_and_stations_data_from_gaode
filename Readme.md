## 1.项目使用

下载或者克隆本项目后在终端中运行main.py文件即可获得湖南省益阳市的公交数据，这是最快捷的方式。

命令为`python .\main.py`

出现的警告可以忽略，也可以自己改一下

如果需要更换为其它城市的数据，可以更改main.py文件中的参数，如下

```python
city = '益阳'
city_phonetic = 'yiyang'
ak = '*******************'  # 这里建议更改为自己的key
```

## 2.文件介绍

+ **get_bus_line_station_data_by_gaode.py**

该文件基于公交网和高德API获取城市的公交线路和站点的原始数据，数据结果保存在csv文件中，如**yiyang_lines.csv**

未获取成功的线路名称会记录在**data not avaliable.log**文件中

+ **line_station_data_to_shp.py**

该文件对csv中的原始数据进行处理，将坐标转换为WGS84坐标，并生成线路和站点的shp文件，shp文件保存在**data文件夹**内，可通过ArcGIS等软件打开，当然Python也可以

## 3.感谢

感谢converter.py的提供者，感谢高德地图，感谢城市数据团？（好像是这个名字，代码是很久以前的，之前是看这个团队的教程视频学会的，感谢）

实际上其余地图厂商也有相应的API，好像百度地图还方便点，没有去弄了

本人代码水平较差，各位轻踩