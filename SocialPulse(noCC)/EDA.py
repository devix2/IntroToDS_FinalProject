import pandas as pd
import numpy as np
from pyecharts.charts import Pie
from pyecharts import options as opts




def Nightingale_Plot(data):
    """
    Creates a plot that counts occurences and prints them on a rose plot nightingale style
    """
    
    #x=data.unique()
    x=list(set(data))  #Estrae elementi unici
    x=np.sort(x)
    y=[]
    for idx,i in enumerate(x):
        y.append((data==i).sum()/500)
    color_series = ['#321AF9','#2812E1','#1A07C1','#1707A9','#1707A9',
                    '#1707A9','#1707A9','#1707A9','#1707A9','#1707A9',
                    '#1707A9','#1707A9','#1707A9','#0A61D0','#0A61D0'
                    '#0A8ED0','#0A8ED0','#0A8ED0','#0ABDDD','#0ABDDD',
                    '#0ABDDD','#0ABDDD','#06F1EE','#06F1EE','#06F1EE',
                    '#06F1EE','#06F1EE','#06F1EE',
                    '#06F1EE','#06F1EE','#06F1EE','#06F1EE','#06F1EE',
                    '#06F1EE','#06F1EE','#06F1EE','#06F1EE','#06F1EE'
                    '#06B4F1','#06B4F1','#06B4F1','#06B4F1','#06B4F1',
                    '#067BF1','#067BF1','#067BF1','#067BF1','#067BF1',
                    ]

    # Instantiate the Pie class
    pie1 = Pie(init_opts=opts.InitOpts(width='950px', height='700px'))
    # Set color
    pie1.set_colors(color_series)
    # Add data, set the radius of the pie chart, whether to display it as a Nightingale chart
    pie1.add("", [list(z) for z in zip(x, y)],
            radius=["30%", "80%"],
            center=["30%", "45%"],
            rosetype="area"
            )
    # Set global configuration items

    #title_opts=opts.TitleOpts(title='rose chart example'),
    #toolbox_opts=opts.ToolboxOpts(),
    pie1.set_global_opts(legend_opts=opts.LegendOpts(is_show=False))
    # Set series configuration items
    pie1.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside", font_size=12,
                                                    formatter="{b}", font_style="italic",
                                                    font_weight="bold", font_family="Microsoft YaHei"
                                                    ),
                     )
    #pie1.render('Test.html')
    return pie1