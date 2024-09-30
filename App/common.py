import sys


# check operating system is win11 or less
def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


# constant: available years selection
AVAILABLE_YEARS: dict = {
    "2019-2020": "2019",
    "2020-2021": "2020",
    "2021-2022": "2021",
    "2022-2023": "2022",
    "2023-2024": "2023",
    "2024-2025": "2024",
    "2025-2026": "2025",
}
