import pandas as pd
import numpy as np

class BollingerBands:
    @staticmethod
    def calculate(rawdf):
        close = rawdf['Close/Last']
        rolling = close.rolling(window=20)
        
        middle_band = rolling.mean()
        std_dev = rolling.std()
        upper_band = middle_band + 2 * std_dev
        lower_band = middle_band - 2 * std_dev
        band_width = upper_band - lower_band
        norm_band_width_pct = (band_width / close) * 100

        return pd.DataFrame({'normBandWdthPct': norm_band_width_pct}, index=rawdf.index)

class ATR:
    @staticmethod
    def calculate(rawdf):
        high, low, close = rawdf['High'], rawdf['Low'], rawdf['Close/Last']
        prev_close = close.shift(1)
        
        true_range = np.maximum.reduce([
            high - low,
            (high - prev_close).abs(),
            (low - prev_close).abs()
        ])
        
        atr = pd.Series(true_range).rolling(window=14).mean()
        scaled_atr_pct = (atr / close) * 100

        return pd.DataFrame({'scaledAtrPct': scaled_atr_pct}, index=rawdf.index)

def createBBWATRmetric(rawdf):
    return pd.DataFrame({'BBWATRmetric': rawdf['normBandWdthPct'] * (rawdf['scaledAtrPct'])})

def main(rawdf):
    bb_df = BollingerBands.calculate(rawdf)
    atr_df = ATR.calculate(rawdf)

    rawdf = rawdf.join(bb_df).join(atr_df)
    voldf = createBBWATRmetric(rawdf)
    voldf['symbol'] = rawdf['symbol']

    return voldf
