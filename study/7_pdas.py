from pandas import Series
date = ["2018-08-01", '2018-08-02', '2018-08-03', '2018-08-04', '2018-08-05']
xrp_close = [512, 508, 512, 507, 500]
s = Series(xrp_close, index=date)
print(s)
print(s.index)
print(s.values)
print(s[['2018-08-02', '2018-08-04']])
print(s['2018-08-01' : '2018-08-03'])
print(s[0:2])

s['2018-08-06'] = 490
print(s.drop('2018-08-01'))
print(s)