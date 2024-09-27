from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect, QHBoxLayout, QScrollArea, QSizePolicy

from qfluentwidgets import IconWidget, FlowLayout, CardWidget, ScrollArea, SingleDirectionScrollArea, SmoothScrollArea
from Modules.UI.stylesheet import StyleSheet
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QSizePolicy


class ButtonCard(CardWidget):
    """ Sample card """

    def __init__(self, icon, title, content, action, parent=None):
        super().__init__(parent=parent)

        self.action = action

        self.iconWidget = IconWidget(icon, self)
        self.iconOpacityEffect = QGraphicsOpacityEffect(self)
        self.iconOpacityEffect.setOpacity(1)  # 设置初始半透明度
        self.iconWidget.setGraphicsEffect(self.iconOpacityEffect)

        self.titleLabel = QLabel(title, self)
        self.titleLabel.setStyleSheet("font-size: 16px; font-weight: 500;")
        self.titleOpacityEffect = QGraphicsOpacityEffect(self)
        self.titleOpacityEffect.setOpacity(1)  # 设置初始半透明度
        self.titleLabel.setGraphicsEffect(self.titleOpacityEffect)
        self.contentLabel = QLabel(content, self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.iconWidget.setFixedSize(32, 32)

        self.hBoxLayout.setSpacing(12)
        self.hBoxLayout.setContentsMargins(18, 10, 10, 10)
        self.vBoxLayout.setSpacing(2)
        self.vBoxLayout.setContentsMargins(4, 4, 4, 4)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)

        self.hBoxLayout.addWidget(self.iconWidget, alignment=Qt.AlignLeft)
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.hBoxLayout.addStretch(1)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.titleLabel, alignment=Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.contentLabel)
        self.vBoxLayout.addStretch(1)

        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')
        self.setMinimumHeight(64)
        self.setMaximumHeight(64)

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        if callable(self.action):
            try:
                self.action(self)
            except Exception as e:
                print(f"执行失败：{e}")
        elif isinstance(self.action, dict):
            pass


class CardList(QWidget):
    """ Sample card view """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Scroll Area
        self.scrollArea = SmoothScrollArea(self)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scrollArea.setWidgetResizable(True)  # Ensure the scroll area resizes with its contents
        self.scrollArea.setStyleSheet("background-color: transparent !important;border: none;")

        # Layout for cards
        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(10)

        # Widget that will hold the layout
        self.widget = QWidget(self)
        self.widget.setLayout(self.vBoxLayout)

        # Ensure widget can expand
        self.widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Set the widget to scroll area
        self.scrollArea.setWidget(self.widget)

        # Main layout of CardList
        layout = QVBoxLayout(self)
        layout.addWidget(self.scrollArea)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Apply stylesheet
        StyleSheet.SAMPLE_CARD.apply(self)

    def clear(self):
        # Remove all widgets from the layout
        for i in reversed(range(self.vBoxLayout.count())):
            widget = self.vBoxLayout.itemAt(i).widget()
            if widget is not None:  # Check if the item is a widget
                widget.deleteLater()  # Safely delete the widget
            self.vBoxLayout.removeItem(self.vBoxLayout.itemAt(i))

    def addCard(self, icon, title, content, action):
        """ Add sample card """
        card = ButtonCard(icon, title, content, action, self)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.vBoxLayout.addWidget(card)
        return card


