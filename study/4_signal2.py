import sys      # sys 모듈 import
from PyQt5.QtWidgets import *       # PyQt5의 GUI 모듈 import
from PyQt5.QtCore import *      # Qtimer, QObject 내장 모듈


class MySignal(QObject):        # 시그널을 보내주는 클래스 정의
    signal1 = pyqtSignal()      # 사용자 시그널 정의 (클래스 내)
    signal2 = pyqtSignal(int, int)

    def run(self):      # 시그널 방출 함수 정의
        self.signal1.emit()     # 시그널 방출 - emit method
        self.signal2.emit(1, 2)


class MyWindow(QMainWindow):  # 윈도우 클래스 정의 QMainWindow의 클래스를 상속
    def __init__(self):  # 초기화자, 객체가 생성될때 자동으로 변수값을 바인딩
        super().__init__()  # 자식클래스에 없는 부모클래스의 method를 사용하기 위한 초기화자 함수

        mysignal = MySignal()  # MySignal 클래스의 객체 생성
        mysignal.signal1.connect(self.signal1_emitted)  # Mysignal 클래스 내 pyqtSignal 클래스의 connect method
        mysignal.signal2.connect(self.signal2_emitted)  # Mysignal 클래스 내 pyqtSignal 클래스의 connect method
        mysignal.run()  # MySignal 클래스 내에 정의한 run method 실행

    @pyqtSlot()  # 데커레이터, 시그널과 슬롯을 연결할 때 데커레이터를 적어주면 더 좋음
    def signal1_emitted(self):  # 사용자 시그널이 방출될때 호출되는 method
        print("signal1 emitted")

    @pyqtSlot(int, int)  # 데커레이터, 시그널과 슬롯을 연결할 때 데커레이터를 적어주면 더 좋음
    def signal2_emitted(self, arg1, arg2):  # 사용자 시그널이 방출될때 호출되는 method
        print("signal2 emitted", arg1, arg2)


app = QApplication(sys.argv)    # QApplication 객체 생성
window = MyWindow()
window.show()
app.exec_()     # 이벤트 루프 생성