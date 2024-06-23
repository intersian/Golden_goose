from pandas import DataFrame

data = {'open': [737, 750, 770], "high": [755, 780, 770], "low": [700, 710, 750], "close": [750, 770, 730]}
df = DataFrame(data, index=["2018-01-01", "2018-01-02", "2018-01-03"])
print(df)


volatility = df["high"] - df["low"]
df["volatility"] = volatility
print(df)