
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
data = pd.read_excel('上海餐饮数据.xlsx',sheetname=0)


data['性价比'] =  (data['口味'] + data['环境'] + data['服务']) / data['人均消费']

# 清除空值和值为0的数据
col_lst = ['口味','人均消费','性价比']
for i in range(1,4):
    locals()['df'+str(i)] = pd.DataFrame({'类别':data['类别'],
                                          col_lst[i-1]:data[col_lst[i-1]]})
    locals()['df'+str(i)] = locals()['df'+str(i)].replace(0,np.nan)
    locals()['df'+str(i)].dropna(inplace=True)
    
# 删除异常数据
def del_error(df,col):
    s = df.describe()
    q1 = s.loc['25%'][col]
    q3 = s.loc['75%'][col]
    IQR = q3 - q1
    mi = q1 - 3*IQR
    ma = q3 + 3*IQR
    return df[(df[col]>mi)&(df[col]<ma)]

df1_re = del_error(df1,'口味')
df2_re = del_error(df2,'人均消费')
df3_re = del_error(df3,'性价比')

# 按类别分组
df_taste = df1_re.groupby(by='类别').mean()
df_price = df2_re.groupby(by='类别').mean()
df_cost_performance = df3_re.groupby(by='类别').mean()

# 标准化及合并
# 口味标准化
df_taste['taste_scale'] = (df_taste['口味']-df_taste['口味'].min())/(df_taste['口味'].max()-df_taste['口味'].min())
# 人均消费越接近均值得分越高，然后标准化
df_price['price_difference'] = np.abs(df_price['人均消费']-df_price['人均消费'].mean())
df_price['price_scale'] = (df_price['price_difference'].max()-df_price['price_difference'])/(df_price['price_difference'].max()-df_price['price_difference'].min())
# 性价比标准化
df_cost_performance['cost_performance_scale'] = (df_cost_performance['性价比']-df_cost_performance['性价比'].min())/(df_cost_performance['性价比'].max()-df_cost_performance['性价比'].min())

# 合并表格
df_merge_01 = pd.merge(df_taste,df_price,left_index=True,right_index=True)
df_merge_02 = pd.merge(df_merge_01,df_cost_performance,left_index=True,right_index=True)
df_merge_02.reset_index(inplace=True)


# bokeh绘图
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool
from bokeh.layouts import column

df_figure_01 = df_merge_02[['类别','taste_scale','cost_performance_scale','人均消费','price_scale']]
df_figure_01.rename(columns={'类别':'category', '人均消费':'price_per'}, inplace = True)
df_figure_01['size'] = df_figure_01['taste_scale'] * 40
source = ColumnDataSource(df_figure_01)
category_lst = df_figure_01['category']

hover = HoverTool(tooltips=[('餐厅类型', '@category'),
                            ('人均消费', '@price_per'),
                            ('性价比得分', '@cost_performance_scale'),
                            ('口味得分', '@taste_scale')])
                       
p1 = figure(plot_width=800, plot_height=300,toolbar_location='above',
            tools=[hover,'box_select,reset,wheel_zoom,pan,crosshair'],
            y_range=[0,1.1],
            title='餐饮类型得分情况')
p1.circle(x = 'price_per',y = 'cost_performance_scale',
          source = source,size = 'size', 
          line_color = 'black', line_dash = [4,4], alpha = 0.3, color = 'blue')



p2 = figure(plot_width=800, plot_height=300,toolbar_location='above',
            tools=[hover,'box_select,reset,wheel_zoom,pan,crosshair'],
            x_range=category_lst,
            title='口味得分')
p2.vbar(x = 'category',top = 'taste_scale',source=source,
        width=0.8,alpha = 0.5, color = 'red')


p3 = figure(plot_width=800, plot_height=300,toolbar_location='above',
            tools=[hover,'box_select,reset,wheel_zoom,pan,crosshair'],
            x_range=category_lst,
            title='人均消费得分（与均值越接近得分越高）')
p3.vbar(x = 'category',top = 'price_scale',source=source,
        width=0.8,alpha = 0.5, color = 'green')

show(column(p1, p2, p3))
