from enum import Enum

from qfluentwidgets import StyleSheetBase, Theme


class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet  """
    SAMPLE_CARD = "sample_card"
    HOME_INTERFACE = "home_interface"

    def path(self, theme=Theme.DARK):
        return f"./resource/qss/{self.value}.qss"

