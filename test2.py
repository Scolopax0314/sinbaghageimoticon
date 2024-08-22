import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, pyqtSignal

class RectangleWindow(QWidget):
    def __init__(self, parent, width, height, x, y, color=Qt.red, thickness=5):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setGeometry(x, y, width, height)

        self.color = color
        self.thickness = thickness

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(self.color, self.thickness)
        painter.setPen(pen)
        painter.drawRect(0, 0, self.width() - self.thickness, self.height() - self.thickness)

# PyQt 애플리케이션 생성
app = QApplication(sys.argv)

# 예시 1: 최상위 위젯으로 생성
window = RectangleWindow(None, 200, 100, 50, 50)
window.show()

# 예시 2: 특정 부모 위젯을 가진 자식 위젯으로 생성
parent_widget = QWidget()
child_window = RectangleWindow(parent_widget, 200, 100, 50, 50)
parent_widget.show()
child_window.show()

# 애플리케이션 이벤트 루프 실행
sys.exit(app.exec_())
