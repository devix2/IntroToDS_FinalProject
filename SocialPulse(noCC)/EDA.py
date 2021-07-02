import pandas as pd
from pyecharts.charts import Pie
from pyecharts import options as opts




def Nightingale_Plot(data)
    """
    Creates a plot that counts occurences and prints them on a rose plot nightingale style
    """
    x=data.unique()
    y=[]
    for idx,i in enumerate(x)
        y[idx]=(data==i).sum()
    
# Prepare data
 provinces = ['Beijing','Shanghai','Heilongjiang','Jilin','Liaoning','Inner Mongolia','Xinjiang','Tibet','Qinghai','Sichuan','Yunnan','Shaanxi' ,'Chongqing',
                           'Guizhou','Guangxi','Hainan','Macao','Hunan','Jiangxi','Fujian','Anhui','Zhejiang','Jiangsu','Ningxia','Shanxi','Hebei ','Tianjin']
num = [1,1,1,17,9,22,23,42,35,7,20,21,16,24,16,21,37,12,13,14,13,7,22,8,16,13,13]
color_series = ['#FAE927','#E9E416','#C9DA36','#9ECB3C','#6DBC49',
                '#37B44E','#3DBA78','#14ADCF','#209AC9','#1E91CA',
                '#2C6BA0','#2B55A1','#2D3D8E','#44388E','#6A368B'
                '#7D3990','#A63F98','#C31C88','#D52178','#D5225B',
                '#D02C2A','#D44C2D','#F57A34','#FA8F2F','#D99D21',
                '#CF7B25','#CF7B25','#CF7B25']
             
   # Create data frame
df = pd.DataFrame({'provinces': provinces, 'num': num})
 # Descending order
df.sort_values(by='num', ascending=False, inplace=True)

 # Extract data 
v = df['provinces'].values.tolist()
d = df['num'].values.tolist()

 # Instantiate the Pie class
pie1 = Pie(init_opts=opts.InitOpts(width='1350px', height='750px'))
 # Set color
pie1.set_colors(color_series)
 # Add data, set the radius of the pie chart, whether to display it as a Nightingale chart
pie1.add("", [list(z) for z in zip(v, d)],
        radius=["30%", "135%"],
        center=["50%", "65%"],
        rosetype="area"
        )
 # Set global configuration items
 pie1.set_global_opts(title_opts=opts.TitleOpts(title='rose chart example'),
                     legend_opts=opts.LegendOpts(is_show=False),
                     toolbox_opts=opts.ToolboxOpts())
 # Set series configuration items
pie1.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside", font_size=12,
                                                                                               formatter="{b}:{c}day", font_style="italic",
                                               font_weight="bold", font_family="Microsoft YaHei"
                                               ),
                     )
 # Generate html document
 pie1.render('Nightingale rose map.html')