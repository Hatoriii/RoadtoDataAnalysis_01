
# 载入模块和读取数据
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bokeh.plotting import figure,show,output_file

from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] # 正常显示负号

import os
os.chdir(r'...\Desktop')
gisdata = pd.read_excel('上海餐饮选址结果.xlsx',sheetname=0)


# 标准化
gisdata['population']=(gisdata['Z']-gisdata['Z'].min())/(gisdata['Z'].max()-gisdata['Z'].min())
gisdata['road']=(gisdata['road_length']-gisdata['road_length'].min())/(gisdata['road_length'].max()-gisdata['road_length'].min())
gisdata['restaurant']=(gisdata['restaurant_count']-gisdata['restaurant_count'].min())/(gisdata['restaurant_count'].max()-gisdata['restaurant_count'].min())
gisdata['competitor']=(gisdata['vegetarian_count'].max()-gisdata['vegetarian_count'])/(gisdata['vegetarian_count'].max()-gisdata['vegetarian_count'].min())
# 综合得分及排序
gisdata['final_score']=gisdata['population']*0.4+gisdata['road']*0.2+gisdata['restaurant']*0.3+gisdata['competitor']*0.1
data_result = gisdata.sort_values(by = 'final_score',ascending=False)
data_result.reset_index()


# bokeh绘图
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool

data_figure_02 = data_result[['lng','lat','final_score']]
data_figure_02['size'] = data_figure_02['final_score']*10
data_figure_02['color'] = ''
data_figure_02['color'].iloc[:10] = 'red'
data_figure_02['color'].iloc[10:] = 'green'
source = ColumnDataSource(data_figure_02)
hover = HoverTool(tooltips=[('经度', '@lng'),
                            ('纬度', '@lat'),
                            ('得分', '@final_score')])
                       
p4 = figure(plot_width=800, plot_height=800,toolbar_location='above',
            tools=[hover,'box_select,reset,wheel_zoom,pan,crosshair'],
            title='空间散点图')
p4.circle(x = 'lng',y = 'lat',
          source = source,size = 'size', 
          line_color = 'black', alpha = 0.8, color = 'color')

show(p4)

