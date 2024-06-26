import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtChart import QLineSeries, QChart, QValueAxis, QDateTimeAxis
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QPainter

class ChartWidget(QWidget):     #QWidget의 클래스를 상속받는 ChartWidget 클래스 생성
    def __init__(self, parent=None, ticker="USDT"):     # parent = 위젯이 그려질 위치 지정, 입력값이 없거나 None의 경우 새로운 창
        super().__init__(parent)
        uic.loadUi("resource/chart.ui", self)       # chart.ui 디자연 적용
        self.ticker = ticker
        self.viewLimit = 128

        self.priceData = QLineSeries()
        # self.priceData.append(0, 10)
        # self.priceData.append(1, 20)
        # self.priceData.append(2, 10)
        self.priceChart = QChart()
        self.priceChart.addSeries(self.priceData)
        self.priceChart.legend().hide()

        axisX = QDateTimeAxis()     #날짜 축 객체 생성
        axisX.setFormat("hh:mm:ss")     #축 표시 형식
        axisX.setTickCount(4)       #표시 시간 개수
        dt = QDateTime.currentDateTime()    #현재 시간 정보 수신
        axisX.setRange(dt, dt.addSecs(self.viewLimit))      #시간축 출력 범위 설정 현재~viewLimit

        axisY = QValueAxis()        #정수 저장 축 생성
        axisY.setVisible(False)     #축 라벨 숨김

        self.priceChart.addAxis(axisX, Qt.AlignBottom)      #생성한 X축을 차트에 연결
        self.priceChart.addAxis(axisY, Qt.AlignRight)      #생성한 Y축을 차트에 연결
        self.priceData.attachAxis(axisX)      #생성한 X축을 데이터에 연결
        self.priceData.attachAxis(axisY)      #생성한 Y축을 데이터에 연결
        self.priceChart.layout().setContentsMargins(0, 0, 0, 0) #차트 여백 최소화

        self.priceView.setChart(self.priceChart)
        self.priceView.setRenderHints(QPainter.Antialiasing)

    def appendData(self, currPrice):
        if len(self.priceData) == self.viewLimit :
            self.priceData.remove(0)    #오래된 0번 인덱스의 데이터 삭제
        dt = QDateTime.currentDateTime()    #현재 시간 정보 수신
        self.priceData.append(dt.toMSecsSinceEpoch(), currPrice)    #현재시간과 현재가를 함께 저장, MSecsSinceEpoch(): QDateTime 객체를 milisecond로 변환
        self.__updateAxis()     #차트에 축 정보를 업데이트

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    cw = ChartWidget()      # 이벤트 루프 중 위젯 생성
    cw.show()
    exit(app.exec_())