import pybithumb
from pybithumb import Bithumb

with open("keys.txt") as f:
    lines = f.readlines()
    bit_key = lines[4].strip()
    bit_secret = lines[5].strip()
    bithumb = pybithumb.Bithumb(bit_key, bit_secret)


# 빗썸 코인 출금 함수

def withdraw_coin(self, withdraw_unit: float, target_address: str, destination_tag_or_memo, withdraw_currency: str,
                  exchange_name: str, cust_type_cd: str, ko_name: str, en_name: str):
    """
    :unit                   : 출금하고자 하는 코인 수량
    :address                : 코인 별 출금 주소
    :destination            : XRP 출금 시 Destination Tag, STEEM 출금 시 입금 메모, XMR 출금 시 Payment ID
    :currency               : 가상자산 영문 코드. 기본값:BTC
    :exchange_name          : 출금 거래소명
    :cust_type_cd           : 개인/법인 여부(개인 01, 법인 02)
    :ko_name                : 개인 수취 정보_국문 성명
    :en_name                : 개인 수취 정보_영문 성명
    """
    resp = None
    try:
        unit = Bithumb._convert_unit(withdraw_unit)
        resp = self.api.withdraw_coin(units=unit,
                                      address=target_address,
                                      destination=destination_tag_or_memo,
                                      currency=withdraw_currency,
                                      exchange_name=exchange_name,
                                      cust_type_cd=cust_type_cd,
                                      ko_name=ko_name,
                                      en_name=en_name)
        return resp['order_id']
    except Exception:
        return resp


aa = bithumb.withdraw_coin(4, "TSHXZ9XySxSrba5jbo1ChAWEvfSHTSty43", "", "USDT")
print(aa)
