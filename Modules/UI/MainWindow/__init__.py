import json

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pyecharts.charts import Bar
from pyecharts.datasets import register_files
from pyecharts.options import InitOpts, TitleOpts, ToolboxOpts, DataZoomOpts
from qfluentwidgets import FluentIcon, InfoBar, InfoBarPosition

from .Ui_MainWindow import Ui_MainWindow, DevConsole
from Modules.constants import AVAILABLE_YEARS
from ...CMS.CMSClient import CMSClient

client = CMSClient()



class MainWindow(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        url = QUrl("file:///resource/template.html")
        # url = QUrl("file:///render.html")
        self.assessments_data = []

        for available_year in AVAILABLE_YEARS.keys():
            self.yearSelect.addItem(available_year)
        self.yearSelect.setCurrentIndex(5)
        self.yearSelect.currentIndexChanged.connect(self.update_subjects)

        self.update_subjects()
        self.chartView.load(url)
        self.chartView.page().runJavaScript(
            '''
                var myChart = echarts.init(document.getElementById('container'), 'light', {renderer: 'canvas'});
            '''
        )
        # self.dev = DevConsole()
        # self.dev.show()
        # self.chartView.page().setDevToolsPage(self.dev.devView.page())

    def update_subjects(self):
        year = self.yearSelect.currentText()
        self.assessments_data = client.get_assessments(year=AVAILABLE_YEARS[year])
        if self.assessments_data is None:
            InfoBar.error(
                title='System Error',
                content=f"Could not fetch subjects based on year {year}!", orient=Qt.Horizontal,
                position=InfoBarPosition.TOP, parent=self
            )
            return

        self.subjectList.clear()

        for subject in self.assessments_data:
            self.subjectList.addCard(icon=FluentIcon.BOOK_SHELF.icon(),
                                     title=subject["subject"],
                                     content=subject["name"],
                                     action=self.update_chartView)

    def get_assessments(self, subject):
        for data in self.assessments_data:
            if data["subject"] == subject:
                return data["assessments"]
        return None

    def update_chartView(self, a):
        self.title.setText(a.titleLabel.text())
        assessments = self.get_assessments(a.titleLabel.text())
        heads = [i["title"] for i in assessments]
        value = [self.get_perc(i["mark"], i["out_of"]) for i in assessments]
        value2 = [self.get_perc(i["average"], i["out_of"]) for i in assessments]
        bar = self.create_bar(heads, value)
        bar.add_yaxis("Average", value2)
        self.reload_canvas(bar.dump_options())

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

    def create_bar(self, head, v):
        bar = Bar(init_opts=InitOpts(theme="essos"), )
        bar.add_xaxis(head)
        bar.add_yaxis("Score", v)
        bar.set_global_opts(title_opts=TitleOpts(title="Score Percentages", subtitle="real value"),
                            toolbox_opts=ToolboxOpts(is_show=True),
                            datazoom_opts=DataZoomOpts(is_show=True, range_start=0, range_end=100))
        return bar

    def reload_canvas(self, options):
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
                var option = eval({options});
                myChart.setOption(option);
            '''
        )
