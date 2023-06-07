from pyecharts import options as opts
from pyecharts.charts import Pie

def pie_base(data, header):
    pie_data = (Pie()
                    .add("", 
                        data,
                        radius=["70%", "80%"],
                        center=["50%", "50%"],
                        rosetype = "radius",
                    )
                    .set_global_opts(
                        title_opts = opts.TitleOpts( title = header + "支出" ),
                        legend_opts = opts.LegendOpts(
                                                        type_ = "scroll",
                                                        pos_left = "85%",
                                                        orient = "vertical",
                                                     ),
                    )
                    .set_series_opts(label_opts = opts.LabelOpts(formatter = "{b}: {c}"))
                )
    pie_base().render("支出.html")

# 是否需要做僅輸出文字的函式?