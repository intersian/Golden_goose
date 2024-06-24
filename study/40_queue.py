import multiprocessing as mp
import websockets
import asyncio
import json
import sys
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


async def bithumb_ws_client(q):  #빗썸 웹소켓 구독 함수
    url = "wss://pubwss.bithumb.com/pub/ws"    #빗썸 웹소켓 서버 주소

    async with websockets.connect(url, ping_interval=None) as websocket:    #빗썸 웹소켓 서버 연결
        subscribe_fmt = {   #빗썸 웹소켓 구독 요청 형식을 파이썬 딕셔너리 형태로 표현
            "type":"ticker",    #ticker(현재가), transaction(체결내역), orderbookdepth(호가) 중 선택
            "symbols": ["USDT_KRW"],    #구독할 코인의 ticker
            "tickTypes": ["1H"]     #30M, 1H, 12H, 24H, MID 중 선택
        }
        subscribe_data = json.dumps(subscribe_fmt)  #수신한 딕셔너리를 json 타입으로 변환
        await websocket.send(subscribe_data)    #구독 요청을 서버에 전송

        while True:     #무한루프 생성
            data = await websocket.recv()       #빗썸 서버에서 데이터 수신
            data = json.loads(data)         #전달받은 json 데이터를 딕셔너리로 변환
            q.put(data)     # 변환된 데이터를 q에 저장

async def main(q):       #main 함수 생성
    await bithumb_ws_client(q)   #빗썸 구독 함수 실행

def producer(q):
    asyncio.run(main(q))

class Consumer(QThread):    #PyQt의 QThread 클래스를 사용하여 스레드 생성
    poped = pyqtSignal(dict)

    def __init__(self, q):
        super().__init__()
        self.q = q

    def run(self):
        while True:
            if not self.q.empty():
                data = q.get()
                self.poped.emit(data)

class MyWindow(QMainWindow):    # UI구성
    def __init__(self,q):
        super().__init__()
        self.setGeometry(200, 200, 400, 200)
        self.setWindowTitle("Bithumb Websocket with PyQt")

        # thread for data consumer
        self.consumer = Consumer(q)
        self.consumer.poped.connect(self.print_data)
        self.consumer.start()

        # widget
        self.label = QLabel("USDT: ", self)
        self.label.move(10, 10)

        # QLineEdit
        self.line_edit = QLineEdit(" ", self)
        self.line_edit.resize(150, 30)
        self.line_edit.move(100, 10)

    @pyqtSlot(dict)
    def print_data(self, data):
        content = data.get('content')
        if content is not None:
            current_price = int(content.get('closePrice'))
            self.line_edit.setText(format(current_price, ",d"))

        now = datetime.datetime.now()
        self.statusBar().showMessage(str(now))

if __name__ == "__main__":
    q = mp.Queue()      #큐 생성
    p = mp.Process(name="Producer", target=producer, args=(q,), daemon=True)    #서브 프로세스 생성, 큐를 함수 인자로 전달
    p.start()

    # Main process
    app = QApplication(sys.argv)    #GUI 프로세스를 실행하는 메인 프로세스 실행
    mywindow = MyWindow(q)
    mywindow.show()
    app.exec_()
