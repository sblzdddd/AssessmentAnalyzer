import sys
from PyQt5.QtWidgets import QApplication, QPlainTextEdit, QScrollArea, QWidget, QVBoxLayout, QLabel

full_text = """First line
Second line
This is the third line, with a lot of words that make this line very long and causes word wrap to come into effect
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaa
bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb bbb
cccccccccccccccccccccccccccccc ccc
dddddddddddddddddddddddddddddd ddd
eeeeeeeeeeeeeeeeeeeeeeeeeeeeee eee
ffffffffffffffffffffffffffffff fff
gggggggggggggggggggggggggggggg ggg
hhhhhhhhhhhhhhhhhhhhhhhhhhhhhh hhh
iiiiiiiiiiiiiiiiiiiiiiiiiiiiii iii
jjjjjjjjjjjjjjjjjjjjjjjjjjjjjj jjj
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk kkk
llllllllllllllllllllllllllllll lll
mmmmmmmmmmmmmmmmmmmmmmmmmmmmmm mmm
nnnnnnnnnnnnnnnnnnnnnnnnnnnnnn nnn
oooooooooooooooooooooooooooooo ooo
pppppppppppppppppppppppppppppp ppp
qqqqqqqqqqqqqqqqqqqqqqqqqqqqqq qqq
rrrrrrrrrrrrrrrrrrrrrrrrrrrrrr rrr
ssssssssssssssssssssssssssssss sss
tttttttttttttttttttttttttttttt ttt
uuuuuuuuuuuuuuuuuuuuuuuuuuuuuu uuu
vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv vvv
wwwwwwwwwwwwwwwwwwwwwwwwwwwwww www
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx xxx
yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy yyy
zzzzzzzzzzzzzzzzzzzzzzzzzzzzzz zzz"""

app = QApplication(sys.argv)

# QScrollArea + QWidget + QVBoxLayout + QLabels = desired layout structure, bad behaviour:
view = QWidget()
layout = QVBoxLayout(view)
layout.setSizeConstraint(QVBoxLayout.SetMinimumSize)

for txt in full_text.split('\n'):
    lbl = QLabel(txt)
    lbl.setWordWrap(True)
    layout.addWidget(lbl)


scroll = QScrollArea()
scroll.setWidget(view)
scroll.setWindowTitle("Bad behaviour, desired layout structure")

scroll.show()
sys.exit(app.exec())