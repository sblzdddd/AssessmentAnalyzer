from PyQt5.QtCore import Qt
from qfluentwidgets import FluentIcon, InfoBar, InfoBarPosition

from .Ui_MainWindow import Ui_MainWindow
from App.CMS import CMSClient
from App.common import AVAILABLE_YEARS


class MainWindow(Ui_MainWindow):
    def __init__(self, client: CMSClient):
        super().__init__()
        self.client: CMSClient = client
        self.assessments_data = []

        # add available years to year combo box
        for available_year in AVAILABLE_YEARS.keys():
            self.yearSelect.addItem(available_year)
        self.yearSelect.setCurrentIndex(5)  # 2024-2025
        # call update_subjects when year select is changed
        self.yearSelect.currentIndexChanged.connect(self.update_subjects)
        # open graph when chart viewer is finished loading
        self.chartView.loadFinished.connect(self.update_subjects)

    def update_subjects(self):
        year = self.yearSelect.currentText()
        # get assessments data
        status, self.assessments_data = self.client.get_assessments(year=AVAILABLE_YEARS[year])
        # fetch info error
        if not status:
            InfoBar.error(
                title=f'Could not fetch subjects',
                content=self.assessments_data, orient=Qt.Horizontal,
                position=InfoBarPosition.TOP, parent=self
            )
            return

        # clear the list
        self.subjectList.clear()

        # add overview card
        c = self.subjectList.addCard(icon=FluentIcon.HOME.icon(),
                                     title="Overview",
                                     content="Overview of all subjects",
                                     action=self.update_chartView)

        # add subjects
        for subject in self.assessments_data:
            self.subjectList.addCard(icon=FluentIcon.BOOK_SHELF.icon(),
                                     title=subject["subject"],
                                     content=subject["name"],
                                     action=self.update_chartView)

        # open overview chart
        self.update_chartView(c)

    # get subject assessments by its name
    def get_assessments(self, subject):
        for data in self.assessments_data:
            if data["subject"] == subject:
                return data["assessments"]
        return None

    # callback if any card is clicked
    def update_chartView(self, a):
        subject_name = a.titleLabel.text()
        self.title.setText(subject_name)
        if subject_name == "Overview":
            self.chartView.create_overview(self.assessments_data)
        else:
            assessments = self.get_assessments(subject_name)
            self.chartView.create_subject_view(assessments)

