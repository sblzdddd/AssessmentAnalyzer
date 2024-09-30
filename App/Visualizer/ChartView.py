from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineDownloadItem
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QFileDialog
from pyecharts.charts import Kline, Line, Grid, Scatter
from pyecharts.options import InitOpts, TitleOpts, ToolboxOpts, DataZoomOpts, TooltipOpts, ToolBoxFeatureOpts, \
    ToolBoxFeatureRestoreOpts, ToolBoxFeatureMagicTypeOpts, ToolBoxFeatureDataViewOpts, MarkPointItem, \
    MarkPointOpts, MarkLineOpts, MarkLineItem, AxisOpts, LabelOpts, GridOpts, AreaStyleOpts, ScatterItem, ItemStyleOpts

from App.Analyzer import calculate_percentage, calculate_quadrants, get_assessment_percentages, calculate_average
from .DevConsole import DevConsole


class ChartView(QWebEngineView):
    def __init__(self):
        self.currentChartData = {}
        super().__init__()
        # render viewer template
        self.load(QUrl("file:///resource/template.html"))
        # initialize echarts.js
        self.page().runJavaScript(
            '''
                var myChart = echarts.init(document.getElementById('container'), 'light', {renderer: 'svg'});
            '''
        )
        # download(save) chart handler
        self.page().profile().downloadRequested.connect(self.handle_download)
        # chrome devTools window
        self.dev = DevConsole()
        # self.dev.show()
        # self.page().setDevToolsPage(self.dev.devView.page())

    # download(save) chart handler
    def handle_download(self, download: QWebEngineDownloadItem):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Graph", download.path())
        if filename:
            download.setPath(filename)
            download.accept()  # Accept the download

    # create subject assessments chart
    def create_subject_view(self, assessments):
        # get percentages for each assessment
        heads, value, average = get_assessment_percentages(assessments)
        # create a line chart instance's options
        self.currentChartData = (
            Line(init_opts=InitOpts(theme='dark'))
            .add_xaxis(heads)
            .add_yaxis(
                series_name="Score",
                y_axis=value,
                markpoint_opts=MarkPointOpts(
                    data=[
                        MarkPointItem(type_="max", name="Score Max"),
                        MarkPointItem(type_="min", name="Score Min"),
                    ]
                ),
                markline_opts=MarkLineOpts(
                    data=[MarkLineItem(type_="average", name="Score Average")]
                )
            )
            .add_yaxis(
                series_name="Average",
                y_axis=average,
                markpoint_opts=MarkPointOpts(
                    data=[
                        MarkPointItem(type_="max", name="Average Max"),
                        MarkPointItem(type_="min", name="Average Min"),
                    ]
                ),
                markline_opts=MarkLineOpts(
                    data=[MarkLineItem(type_="average", name="Average Average")]
                )
            )
            .set_series_opts(
                areastyle_opts=AreaStyleOpts(opacity=0.3),
            )
            .set_global_opts(title_opts=TitleOpts(title="Score Percentages"),
                             toolbox_opts=ToolboxOpts(is_show=True,
                                                      feature=ToolBoxFeatureOpts(
                                                          restore=ToolBoxFeatureRestoreOpts(is_show=False),
                                                      ),
                                                      orient='vertical',
                                                      pos_left="93%", ),
                             tooltip_opts=TooltipOpts(trigger='axis', axis_pointer_type="cross"),
                             datazoom_opts=DataZoomOpts(is_show=True, range_start=0, range_end=100),
                             yaxis_opts=AxisOpts(min_=0, max_=100, position="left",
                                                 axislabel_opts=LabelOpts(formatter="{value} %"),
                                                 ))
        ).dump_options()
        # re-render
        self.reload_canvas()

    def create_overview(self, assessments_data):
        perc = []
        avr = []
        # calculate distributions (max, min, average, 1st and 3st quadrant) for each subjects
        for data in assessments_data:
            marks = []
            for i in data["assessments"]:
                p = calculate_percentage(i["mark"], i["out_of"])
                if p != 0:
                    marks.append(p)
            perc.append(calculate_quadrants(marks))
            avr.append(ScatterItem(value=calculate_average(marks), symbol='rect', symbol_size=[10, 2]))

        # create a Candlestick/KLine chart instance
        kline = (
            Kline(init_opts=InitOpts(theme='dark'))
            .add_xaxis([data["subject"] for data in assessments_data])
            .add_yaxis("Score", perc)
            .set_global_opts(title_opts=TitleOpts(title="Subject Scores Distribution"),
                             toolbox_opts=ToolboxOpts(is_show=True,
                                                      feature=ToolBoxFeatureOpts(
                                                          restore=ToolBoxFeatureRestoreOpts(is_show=False),
                                                          magic_type=ToolBoxFeatureMagicTypeOpts(is_show=False),
                                                          data_view=ToolBoxFeatureDataViewOpts(is_show=False))),
                             tooltip_opts=TooltipOpts(trigger='axis', axis_pointer_type="cross"),
                             datazoom_opts=DataZoomOpts(is_show=True, range_start=0, range_end=100),
                             yaxis_opts=AxisOpts(min_=0, max_=100, position="left",
                                                 axislabel_opts=LabelOpts(formatter="{value} %"),
                                                 )
                             )
        )
        # create a scatter chart instance for displaying averages
        scatter = (
            Scatter()
            .add_xaxis([data["subject"] for data in assessments_data])
            .add_yaxis("Average", avr, color='#5affb4')
            .set_series_opts(
                label_opts=LabelOpts(is_show=False),
                itemstyle_opts=ItemStyleOpts(color='#5affb4')
            )
        )

        # overlap two charts
        overlap = kline.overlap(scatter)

        grid = Grid()
        grid.add(overlap, GridOpts(), is_control_axis_index=True)
        self.currentChartData = grid.dump_options()

        # re-render
        self.reload_canvas()

    # re-render canvas
    def reload_canvas(self):
        self.page().runJavaScript(
            f'''
                // dispose old charts
                try {{
                    myChart.dispose();
                }} catch {{}}
                // reset chart
                var myChart = echarts.init(document.getElementById('container'), 'dark', {{renderer: 'canvas'}});
                window.addEventListener('resize', function() {{
                  myChart.resize();
                }});
                // clear chart
                myChart.clear();
                // transmit option
                var option = eval({self.currentChartData});
                // set option & render
                myChart.setOption(option);
            '''
        )
