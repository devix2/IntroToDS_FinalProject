import pandas as pd
from pyecharts.charts import Pie
from pyecharts import options as opts

# Prepare data
provinces = [10,1,3,4,10,1,3,4,10,1,3,4,10,1,3,4,10,1,3,4,10,1,3,4,10,1,3,4,10,1,3,4,10,1,3,4,10,1,3,4,10,1,3,4,10,1,3,4]
num = [10,1,3,4,10,1,3,4,10,1,3,4,10,1,3,4,10,1,3,4,10,1,3,4,10,1,3,4,10,1,3,4,10,1,3,4,10,1,3,4,10,1,3,4,10,1,3,4]
#color_series = ['#FAE927','#E9E416','#C9DA36','#9ECB3C']
            
# Create data frame
#df = pd.DataFrame({'provinces': provinces, 'num': num})
# Descending order
#df.sort_values(by='num', ascending=False, inplace=True)

# Extract data 
#v = df['provinces'].values.tolist()
#d = df['num'].values.tolist()

v=provinces
d=num
print(v)
print(d)


# Instantiate the Pie class
pie1 = Pie(init_opts=opts.InitOpts(width='1350px', height='750px'))
# Set color
#pie1.set_colors(color_series)
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
