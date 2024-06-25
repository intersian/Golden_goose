import websockets
import asyncio
import json


async def bithumb_ws_client():  #빗썸 웹소켓 구독 함수
    url = "wss://pubwss.bithumb.com/pub/ws"     #빗썸 웹소켓 서버 주소

    async with websockets.connect(url, ping_interval=None) as websocket:    #빗썸 웹소켓 서버 연결
        greeting = await websocket.recv()   #빗썸 웹소켓 서버에서 데이터 수신
        print(greeting)     #빗썸 웹소켓 서버에서 수신한 데이터 출력

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
            print(data)     # 딕셔너리 출력

async def main():       #main 함수 생성
    await bithumb_ws_client()   #빗썸 구독 함수 실행

asyncio.run(main())     #이벤트 루프를 생성, main 코루틴 처리 후 이벤트 closing