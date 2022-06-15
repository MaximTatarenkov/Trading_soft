from datetime import datetime, date, timedelta

from main import run, TIME_ZONE
from rates.bars import Rates
from .db import session



S_AND_P = ["MMM", "AOS", "ABT", "ABBV", "ABMD", "ACN", "ATVI", "ADM", "ADBE", "AAP", "AMD", "AES", "AFL", "A", "APD", "AKAM", "ALB", "ALK", "ARE", "ALGN",
           "ALLE", "LNT", "ALL", "GOOGL", "GOOG", "MO", "AMZN", "AMCR", "AEE", "AAL", "AEP", "AXP", "AIG", "AMT", "AWK", "AMP", "ABC", "AME", "AMGN", "APH",
           "ADI", "ANSS", "ANTM", "AON", "APA", "AAPL", "AMAT", "APTV", "ANET", "AJG", "AIZ", "T", "ATO", "ADSK", "ADP", "AZO", "AVB", "AVY", "BKR", "BLL",
           "BAC", "BBWI", "BAX", "BDX", "BRK.B", "BBY", "BIO", "TECH", "BIIB", "BLK", "BK", "BA", "BKNG", "BWA", "BXP", "BSX", "BMY", "AVGO", "BR", "BRO",
           "BF.B", "CHRW", "CDNS", "CZR", "CPB", "COF", "CAH", "KMX", "CCL", "CARR", "CTLT", "CAT", "CBOE", "CBRE", "CDW", "CE", "CNC", "CNP", "CDAY",
           "CERN", "CF", "CRL", "SCHW", "CHTR", "CVX", "CMG", "CB", "CHD", "CI", "CINF", "CTAS", "CSCO", "C", "CFG", "CTXS", "CLX", "CME", "CMS", "KO",
           "CTSH", "CL", "CMCSA", "CMA", "CAG", "COP", "ED", "STZ", "CPRT", "GLW", "CTVA", "COST", "CTRA", "CCI", "CSX", "CMI", "CVS", "DHI", "DHR", "DRI",
           "DVA", "DE", "DAL", "XRAY", "DVN", "DXCM", "FANG", "DLR", "DFS", "DISCA", "DISCK", "DISH", "DG", "DLTR", "D", "DPZ", "DOV", "DOW", "DTE", "DUK",
           "DRE", "DD", "DXC", "EMN", "ETN", "EBAY", "ECL", "EIX", "EW", "EA", "LLY", "EMR", "ENPH", "ETR", "EOG", "EFX", "EQIX", "EQR", "ESS", "EL",
           "ETSY", "RE", "EVRG", "ES", "EXC", "EXPE", "EXPD", "EXR", "XOM", "FFIV", "FB", "FAST", "FRT", "FDX", "FIS", "FITB", "FRC", "FE", "FISV", "FLT",
           "FMC", "F", "FTNT", "FTV", "FBHS", "FOXA", "FOX", "BEN", "FCX", "GPS", "GRMN", "IT", "GNRC", "GD", "GE", "GIS", "GM", "GPC", "GILD", "GPN",
           "GL", "GS", "HAL", "HBI", "HAS", "HCA", "PEAK", "HSIC", "HES", "HPE", "HLT", "HOLX", "HD", "HON", "HRL", "HST", "HWM", "HPQ", "HUM", "HBAN",
           "HII", "IBM", "IEX", "IDXX", "INFO", "ITW", "ILMN", "INCY", "IR", "INTC", "ICE", "IFF", "IP", "IPG", "INTU", "ISRG", "IVZ", "IPGP", "IQV",
           "IRM", "JBHT", "JKHY", "J", "SJM", "JNJ", "JCI", "JPM", "JNPR", "KSU", "K", "KEY", "KEYS", "KMB", "KIM", "KMI", "KLAC", "KHC", "KR", "LHX",
           "LH", "LRCX", "LW", "LVS", "LEG", "LDOS", "LEN", "LNC", "LIN", "LYV", "LKQ", "LMT", "L", "LOW", "LUMN", "LYB", "MTB", "MRO", "MPC", "MKTX",
           "MAR", "MMC", "MLM", "MAS", "MA", "MTCH", "MKC", "MCD", "MCK", "MDT", "MRK", "MET", "MTD", "MGM", "MCHP", "MU", "MSFT", "MAA", "MRNA", "MHK",
           "TAP", "MDLZ", "MPWR", "MNST", "MCO", "MS", "MSI", "MSCI", "NDAQ", "NTAP", "NFLX", "NWL", "NEM", "NWSA", "NWS", "NEE", "NLSN", "NKE", "NI",
           "NSC", "NTRS", "NOC", "NLOK", "NCLH", "NRG", "NUE", "NVDA", "NVR", "NXPI", "ORLY", "OXY", "ODFL", "OMC", "OKE", "ORCL", "OGN", "OTIS",
           "PCAR", "PKG", "PH", "PAYX", "PAYC", "PYPL", "PENN", "PNR", "PBCT", "PEP", "PKI", "PFE", "PM", "PSX", "PNW", "PXD", "PNC", "POOL", "PPG",
           "PPL", "PFG", "PG", "PGR", "PLD", "PRU", "PTC", "PEG", "PSA", "PHM", "PVH", "QRVO", "QCOM", "PWR", "DGX", "RL", "RJF", "RTX", "O", "REG",
           "REGN", "RF", "RSG", "RMD", "RHI", "ROK", "ROL", "ROP", "ROST", "RCL", "SPGI", "CRM", "SBAC", "SLB", "STX", "SEE", "SRE", "NOW", "SHW",
           "SPG", "SWKS", "SNA", "SO", "LUV", "SWK", "SBUX", "STT", "STE", "SYK", "SIVB", "SYF", "SNPS", "SYY", "TMUS", "TROW", "TTWO", "TPR", "TGT",
           "TEL", "TDY", "TFX", "TER", "TSLA", "TXN", "TXT", "COO", "HIG", "HSY", "MOS", "TRV", "DIS", "TMO", "TJX", "TSCO", "TT", "TDG", "TRMB",
           "TFC", "TWTR", "TYL", "TSN", "USB", "UDR", "ULTA", "UAA", "UA", "UNP", "UAL", "UPS", "URI", "UNH", "UHS", "VLO", "VTR", "VRSN", "VRSK",
           "VZ", "VRTX", "VFC", "VIAC", "VTRS", "V", "VNO", "VMC", "WRB", "GWW", "WAB", "WBA", "WMT", "WM", "WAT", "WEC", "WFC", "WELL", "WST", "WDC",
           "WU", "WRK", "WY", "WHR", "WMB", "WLTW", "WYNN", "XEL", "XLNX", "XYL", "YUM", "ZBRA", "ZBH", "ZION", "ZTS"]


class Filling(Rates):

    def get_first_bar(self):
        old_year = 1970
        past_date = datetime(old_year, 1, 1, tzinfo=TIME_ZONE)
        first_bar = self.get_bars_from(past_date, 10)
        date = first_bar["time"][0]
        return date

    def get_range(self):
        first_bar = self.get_first_bar()
        while first_bar < datetime.now():
            date_from = first_bar
            date_to = first_bar + timedelta(weeks=10)
            if date_to > datetime.now():
                date_to = datetime.now()
            bar_range = self.get_bars_range(date_from, date_to)
            first_bar += timedelta(weeks=10)

    def save_to_db(self, bars):
        pass





if __name__=="__main__":
    run()
    fil = Filling("MMM", "d1")
    print(fil.get_first_bar())



# date_from = datetime(2011, 9, 30, tzinfo=TIME_ZONE)
# rates = Rates(symbol="BTCUSD", time_frame="m5", bars_count=50, date_from=date_from)
# bars = rates.get_bars_from()
# print(bars)
