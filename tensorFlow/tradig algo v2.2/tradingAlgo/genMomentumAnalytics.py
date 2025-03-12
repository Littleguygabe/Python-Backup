import pandas as pd

class candleSticks:
    @staticmethod
    def calculate(df):
        return df.assign(
            candlesticksABS=(df['Close/Last'] - df['Open']).abs(),
            scaledCandleSticks=lambda x: (x['candlesticksABS'] / x['Close/Last']) * 100,
            scaldCndlStks20dAvg=lambda x: x['scaledCandleSticks'].rolling(window=20).mean()
        )

class volume:
    @staticmethod
    def calculate(df):
        return df.assign(
            volTraded20EMA=df['Volume'].ewm(span=20, adjust=False).mean(),
            vol20dEMAdiff=lambda x: ((x['Volume'] - x['volTraded20EMA']) / x['volTraded20EMA']) * 100
        )

def calcVolCsMetric(df):
    df['volCsMetric'] = df['scaldCndlStks20dAvg'] * df['vol20dEMAdiff']
    return df[['symbol', 'volCsMetric']]

def main(df):
    df = candleSticks.calculate(df)
    df = volume.calculate(df)
    return calcVolCsMetric(df)
