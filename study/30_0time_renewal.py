import datetime
import time

dt = datetime.datetime(2018, 12, 1)
# print(dt)
# print(dt.year, dt.month, dt.day)
now = datetime.datetime.now()
# print(now)
# print(now == dt)
# print(now > dt)

mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
# print(now)
# print(mid)

while True:
    now = datetime.datetime.now()
    # if now == mid:
    if mid < now < mid + datetime.timedelta(seconds=10):
        print("정각입니다")
        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

    print(now, "vs", mid)
    time.sleep(1)