import pandas as pd
import numpy as np
import make_dataset as m_d
import json

#Questa la rimuovo in caso serva eseguire lo script senza aver pyecharts
    #Il grafico lo ho salvato ad immagine
"""
from pyecharts.charts import Pie
from pyecharts import options as opts
def Nightingale_Plot(data):
    """"""
    Creates a plot that counts occurences and prints them on a rose plot nightingale style
    """"""
    
    
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
    """


def tempDistrib():
    """
    Funzione che fetcha la distribuzione della temperatura a partire dal database weather
    Ovviamente i dati della temperatura non sono propriamente scorrelati da posizione geografica
    o ora del giorno... Questa è da vedersi come stima, tutti questi dati sono in un certo modo correlati
    """

    weather_json = json.load( open(m_d.data_path_in / m_d.files['weather'][0]) )
    weather = pd.DataFrame(weather_json['features'])

    colnames=["temperatures.%02d%02d"%(int(np.floor(i/4)),(i%4)*15) for i in range(0,96)]
    
    temperatures=weather[colnames]
    out=[]
    for i in colnames:
        out.extend(list(temperatures[i]))
    
    return out


