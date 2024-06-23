from pandas import Series

s = Series([100, 200, 300])
s2 = s.shift(1)
s3 = s2.shift(-1)
print(s)
print(s2)
print(s3)
