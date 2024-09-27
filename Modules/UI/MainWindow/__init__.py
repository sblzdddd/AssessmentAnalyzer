import json

from PyQt5.QtCore import QUrl, Qt
from pyecharts.charts import Bar, Kline
from pyecharts.options import InitOpts, TitleOpts, ToolboxOpts, DataZoomOpts, TooltipOpts
from qfluentwidgets import FluentIcon, InfoBar, InfoBarPosition
import numpy as np

from .Ui_MainWindow import Ui_MainWindow, DevConsole
from Modules.constants import AVAILABLE_YEARS
from ...CMS.CMSClient import CMSClient


class MainWindow(Ui_MainWindow):
    def __init__(self, client: CMSClient):
        super().__init__()
        self.client: CMSClient = client
        self.assessments_data = []
        self.currentChartData = {}

        for available_year in AVAILABLE_YEARS.keys():
            self.yearSelect.addItem(available_year)
        self.yearSelect.setCurrentIndex(5)
        self.yearSelect.currentIndexChanged.connect(self.update_subjects)

        # self.update_subjects()
        self.chartView.load(QUrl("file:///resource/template.html"))
        self.chartView.page().runJavaScript(
            '''
                var myChart = echarts.init(document.getElementById('container'), 'light', {renderer: 'canvas'});
            '''
        )
        self.chartView.loadFinished.connect(self.update_subjects)
        # self.dev = DevConsole()
        # self.dev.show()
        # self.chartView.page().setDevToolsPage(self.dev.devView.page())

    def update_subjects(self):
        year = self.yearSelect.currentText()
        status, self.assessments_data = self.client.get_assessments(year=AVAILABLE_YEARS[year])
        if not status:
            InfoBar.error(
                title=f'Could not fetch subjects',
                content=self.assessments_data, orient=Qt.Horizontal,
                position=InfoBarPosition.TOP, parent=self
            )
            return

        self.subjectList.clear()

        c = self.subjectList.addCard(icon=FluentIcon.BOOK_SHELF.icon(),
                                     title="Overview",
                                     content="Overview of all subjects",
                                     action=self.update_chartView)

        for subject in self.assessments_data:
            self.subjectList.addCard(icon=FluentIcon.BOOK_SHELF.icon(),
                                     title=subject["subject"],
                                     content=subject["name"],
                                     action=self.update_chartView)

        self.update_chartView(c)

    def get_assessments(self, subject):
        for data in self.assessments_data:
            if data["subject"] == subject:
                return data["assessments"]
        return None

    def update_chartView(self, a):
        subject_name = a.titleLabel.text()
        self.title.setText(subject_name)
        if subject_name == "Overview":
            self.create_overview()
        else:
            self.create_subject_view(subject_name)
        self.reload_canvas()

    def create_subject_view(self, subject_name):
        assessments = self.get_assessments(subject_name)
        heads = [i["title"] for i in assessments]
        value = [self.get_perc(i["mark"], i["out_of"]) for i in assessments]
        average = [self.get_perc(i["average"], i["out_of"]) for i in assessments]

        bar = Bar(init_opts=InitOpts(theme='dark'))
        bar.set_global_opts(title_opts=TitleOpts(title="Score Percentages", subtitle="real value"),
                            toolbox_opts=ToolboxOpts(is_show=True), tooltip_opts=TooltipOpts(trigger='axis'),
                            datazoom_opts=DataZoomOpts(is_show=True, range_start=0, range_end=100))
        bar.add_xaxis(heads)
        bar.add_yaxis("Score", value)
        bar.add_yaxis("Average", average)
        self.currentChartData = bar.dump_options()

    def calculate_quadrants(self, data):
        if len(data) < 1:
            return [0, 0, 0, 0]
        lowest = np.min(data)
        highest = np.max(data)
        first_quartile = np.percentile(data, 25)
        third_quartile = np.percentile(data, 75)
        return [first_quartile, third_quartile, lowest, highest]

    def create_overview(self):
        kline = Kline(init_opts=InitOpts(theme='dark'))
        kline.set_global_opts(title_opts=TitleOpts(title="Score Percentages", subtitle="real value"),
                              toolbox_opts=ToolboxOpts(is_show=True), tooltip_opts=TooltipOpts(trigger='axis'),
                              datazoom_opts=DataZoomOpts(is_show=True, range_start=0, range_end=100))
        kline.add_xaxis([data["subject"] for data in self.assessments_data])

        perc = []
        for data in self.assessments_data:
            marks = []
            for i in data["assessments"]:
                p = self.get_perc(i["mark"], i["out_of"])
                if p != 0:
                    marks.append(p)
            perc.append(self.calculate_quadrants(marks))

        kline.add_yaxis("Score", perc)
        self.currentChartData = kline.dump_options()

    def get_perc(self, mark, out_of):
        try:
            return round(float(mark) / float(out_of), 2) * 100
        except ZeroDivisionError:
            return 0
        except ValueError:
            return 0
        except TypeError:
            return 0
        except:
            return 0

    def reload_canvas(self):
        self.chartView.page().runJavaScript(
            f'''
                try {{
                    myChart.dispose();
                }} catch {{}}
                var myChart = echarts.init(document.getElementById('container'), 'dark', {{renderer: 'canvas'}});
                window.addEventListener('resize', function() {{
                  myChart.resize();
                }});
                myChart.clear();
                var option = eval({self.currentChartData});
                myChart.setOption(option);
            '''
        )
