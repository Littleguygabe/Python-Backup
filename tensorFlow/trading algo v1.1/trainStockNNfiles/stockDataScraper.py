import yfinance as yf
import pandas as pd

tickers = [
    "AAPL",  # Apple Inc.
    "MSFT",  # Microsoft Corporation
    "AMZN",  # Amazon.com, Inc.
    "NVDA",  # NVIDIA Corporation
    "GOOGL", # Alphabet Inc. (Class A)
    "GOOG",  # Alphabet Inc. (Class C)
    "META",  # Meta Platforms, Inc.
    "TSLA",  # Tesla, Inc.
    "AVGO",  # Broadcom Inc.
    "PEP",   # PepsiCo, Inc.
    "COST",  # Costco Wholesale Corporation
    "ADBE",  # Adobe Inc.
    "CSCO",  # Cisco Systems, Inc.
    "NFLX",  # Netflix, Inc.
    "INTC",  # Intel Corporation
    "TXN",   # Texas Instruments Incorporated
    "AMD",   # Advanced Micro Devices, Inc.
    "QCOM",  # QUALCOMM Incorporated
    "AMAT",  # Applied Materials, Inc.
    "HON",   # Honeywell International Inc.
    "SBUX",  # Starbucks Corporation
    "INTU",  # Intuit Inc.
    "ISRG",  # Intuitive Surgical, Inc.
    "BKNG",  # Booking Holdings Inc.
    "MDLZ",  # Mondelez International, Inc.
    "AMGN",  # Amgen Inc.
    "ADI",   # Analog Devices, Inc.
    "GILD",  # Gilead Sciences, Inc.
    "MU",    # Micron Technology, Inc.
    "LRCX",  # Lam Research Corporation
    "REGN",  # Regeneron Pharmaceuticals, Inc.
    "FISV",  # Fiserv, Inc.
    "ATVI",  # Activision Blizzard, Inc.
    "ADP",   # Automatic Data Processing, Inc.
    "CSX",   # CSX Corporation
    "MRNA",  # Moderna, Inc.
    "PANW",  # Palo Alto Networks, Inc.
    "VRTX",  # Vertex Pharmaceuticals Incorporated
    "KDP",   # Keurig Dr Pepper Inc.
    "MAR",   # Marriott International, Inc.
    "ADSK",  # Autodesk, Inc.
    "MELI",  # MercadoLibre, Inc.
    "LULU",  # Lululemon Athletica Inc.
    "SNPS",  # Synopsys, Inc.
    "ORLY",  # O'Reilly Automotive, Inc.
    "KLAC",  # KLA Corporation
    "IDXX",  # IDEXX Laboratories, Inc.
    "MNST",  # Monster Beverage Corporation
    "CTAS",  # Cintas Corporation
    "AEP",   # American Electric Power Company, Inc.
    "PAYX",  # Paychex, Inc.
    "XEL",   # Xcel Energy Inc.
    "ROST",  # Ross Stores, Inc.
    "PCAR",  # PACCAR Inc
    "TEAM",  # Atlassian Corporation Plc
    "SGEN",  # Seagen Inc.
    "ASML",  # ASML Holding N.V.
    "SWKS",  # Skyworks Solutions, Inc.
    "BIDU",  # Baidu, Inc.
    "WDAY",  # Workday, Inc.
    "CDNS",  # Cadence Design Systems, Inc.
    "NXPI",  # NXP Semiconductors N.V.
    "SPLK",  # Splunk Inc.
    "VRSK",  # Verisk Analytics, Inc.
    "ANSS",  # ANSYS, Inc.
    "EBAY",  # eBay Inc.
    "ALGN",  # Align Technology, Inc.
    "PDD",   # Pinduoduo Inc.
    "MTCH",  # Match Group, Inc.
    "OKTA",  # Okta, Inc.
    "CPRT",  # Copart, Inc.
    "CHTR",  # Charter Communications, Inc.
    "DDOG",  # Datadog, Inc.
    "ZS",    # Zscaler, Inc.
    "DOCU",  # DocuSign, Inc.
    "CRWD",  # CrowdStrike Holdings, Inc.
    "BIIB",  # Biogen Inc.
    "SIRI",  # Sirius XM Holdings Inc.
    "VRSN",  # VeriSign, Inc.
    "MCHP",  # Microchip Technology Incorporated
    "CTSH",  # Cognizant Technology Solutions Corporation
    "DLTR",  # Dollar Tree, Inc.
    "EXC",   # Exelon Corporation
    "GEHC",  # GE HealthCare Technologies Inc.
    "FAST",  # Fastenal Company
    "TTD",   # The Trade Desk, Inc.
    "CEG",   # Constellation Energy Corporation
    "LCID",  # Lucid Group, Inc.
    "BKR",   # Baker Hughes Company
    "FTNT",  # Fortinet, Inc.
    "ABNB",  # Airbnb, Inc.
    "KHC",   # The Kraft Heinz Company
    "WBD",   # Warner Bros. Discovery, Inc.
    "MRVL",  # Marvell Technology, Inc.
    "ON",    # ON Semiconductor Corporation
    "BIDU",  # Baidu, Inc.
    "ZM",    # Zoom Video Communications, Inc.
    "LULU",  # Lululemon Athletica Inc.
    "ROKU",  # Roku, Inc.
    "PDD",   # Pinduoduo Inc.
    "JD",    # JD.com, Inc.
    "NTES",  # NetEase, Inc.
    "CPRT",  # Copart, Inc.
    "SGEN",  # Seagen Inc.
    "VRSK",  # Verisk Analytics, Inc.
    "ANSS",  # ANSYS, Inc.
    "ASML",  # ASML Holding N.V.
    "NXPI",  # NXP Semiconductors N.V.
    "CDNS",  # Cadence Design Systems, Inc.
    "KLAC",  # KLA Corporation
    "SNPS",  # Synopsys, Inc.
    "MELI",  # MercadoLibre, Inc.
    "ORLY",  # O'Reilly Automotive, Inc.
    "IDXX",  # IDEXX Laboratories, Inc.
    "ROST",  # Ross Stores, Inc.
    "PCAR",  # PACCAR Inc
    "PAYX",  # Paychex, Inc.
    "XEL",   # Xcel Energy Inc.
    "CTAS",  # Cintas Corporation
    "AEP",   # American Electric Power Company, Inc.
    "MNST",  # Monster Beverage Corporation
    "MAR",   # Marriott International, Inc.
    "KDP",   # Keurig Dr Pepper Inc.
]
for ticker in tickers:
    stock = yf.Ticker(ticker)
    df = stock.history(period="10y")
    
    df = df.reset_index()
    df = df.rename(columns={
        "Date": "Date",
        "Open": "Open",
        "High": "High",
        "Low": "Low",
        "Close": "Close/Last",
        "Volume": "Volume"
    })


    df = df.drop(columns=["Adj Close"], errors="ignore")
    df.insert(0, "symbol", ticker)
    df["Date"] = pd.to_datetime(df["Date"])  # Convert to datetime
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")  # Format as string

    df = df[::-1]


    df.to_csv(f"nasdaq100/{ticker}.csv", index=False)

    print(f"Retrieved {ticker}")

print("All files saved")

