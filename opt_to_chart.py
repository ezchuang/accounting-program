import pyecharts
from pyecharts import options as opts
from pyecharts.charts import Pie
1
def pie_base(data, header):
    pie_data = (
        Pie()\
        .add("", data, radius=["30%", "60%"], center=["40%", "50%"],)
        .set_global_opts(
            title_opts = opts.TitleOpts( title = header ),
            legend_opts = opts.LegendOpts(
                type_ = "scroll",
                pos_left = "75%",
                orient = "vertical",
            ),
        )
        .set_series_opts(label_opts = opts.LabelOpts(formatter = "{b}: {c}"),\
                         tooltip_opts=opts.TooltipOpts(trigger="item", formatter= "{b}: {c} ({d}%)"),)
    )
    pie_data.render(header+".html")
    
    return

# 是否需要做僅輸出文字的函式?