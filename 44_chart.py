import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtChart import QLineSeries, QChart

class ChartWidget(QWidget):     #QWidget의 클래스를 상속받는 ChartWidget 클래스 생성
    def __init__(self, parent=None, ticker="USDT"):     # parent = 위젯이 그려질 위치 지정, 입력값이 없거나 None의 경우 새로운 창
        super().__init__(parent)
        uic.loadUi("resource/chart.ui", self)       # chart.ui 디자연 적용
        self.ticker = ticker
        self.viewLimit = 128

        self.priceData = QLineSeries()
        self.priceData.append(0, 10)
        self.priceData.append(1, 20)
        self.priceData.append(2, 10)

        self.priceChart = QChart()
        self.priceChart.addSeries(self.priceData)

        self.priceView.setChart(self.priceChart)

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    cw = ChartWidget()      # 이벤트 루프 중 위젯 생성
    cw.show()
    exit(app.exec_())