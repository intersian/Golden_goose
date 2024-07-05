import uuid
import jwt
import pybithumb
import pyupbit


with open("keys.txt") as f:
    lines = f.readlines()
    bit_key = lines[0].strip()
    bit_secret = lines[1].strip()
    bithumb = pybithumb.Bithumb(bit_key, bit_secret)

    up_key = lines[2].strip()
    up_secret = lines[3].strip()
    upbit = pyupbit.Upbit(up_key, up_secret)

def transfer_bithumb_to_upbit(amount, address):
    currency = "USDT"
    destination = address  # 업비트의 USDT 지갑 주소
    response = bithumb.bithumb_private_api('/trade/btc_withdrawal', {
        'currency': currency,
        'units': amount,
        'address': destination,
    })
    return response

transfer_bithumb_to_upbit(4, upbit_wallet_address)