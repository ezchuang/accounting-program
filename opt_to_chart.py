from pyecharts import options as opts
from pyecharts.charts import Pie

def pie_base(data, header):
    pie_data = (
        Pie()\
        .add(
            "",
            data,
            radius=["30%", "50%"],
            center=["40%", "50%"],
            rosetype = "radius",
        )
        .set_global_opts(
            title_opts = opts.TitleOpts( title = header ),
            legend_opts = opts.LegendOpts(
                type_ = "scroll",
                pos_left = "85%",
                orient = "vertical",
            ),
        )
        .set_series_opts(label_opts = opts.LabelOpts(formatter = "{b}: {c}"))
    )
    pie_data.render(header+".html")
    
    return

# 是否需要做僅輸出文字的函式?