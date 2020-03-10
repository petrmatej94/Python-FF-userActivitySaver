import psycopg2

# Script pro vytvoreni 28 tabulek v DB. Muze byt zmeneno na DROP TABLE
# Otazkou bylo, jestli mit jednu velkou tabulku vseho dohromady nebo 28 tabulek jednotlivych paru
# Jedna tabulka -->
# + Muzu udelat select nad vsim co obsahuje napr. AUD
# - Nemam unikatni datum
# - Hure se bude delat vyplneni dat, ktere chybi (zaplneni mezer)


con = psycopg2.connect(
    host="<IP...>",
    database="<DBNAME>",
    user="<ADMINNAME>",
    password="<PASSWORD>"
)


pairs = ["EURUSD", "GBPUSD", "USDCHF", "AUDUSD", "NZDUSD", "USDCAD", "USDJPY",
           "EURGBP", "GBPCHF", "GBPAUD", "GBPNZD", "GBPCAD", "GBPJPY",
           "EURCHF", "EURAUD", "EURNZD", "EURCAD", "EURJPY",
           "AUDCHF", "NZDCHF", "CADCHF", "CHFJPY",
           "AUDCAD", "NZDCAD", "CADJPY",
           "AUDNZD", "NZDJPY",
           "AUDJPY"]


cur = con.cursor()

for pair in pairs:
    cur.execute(f"""
    
CREATE TABLE {pair} (
    record_id serial PRIMARY KEY,
    date timestamp UNIQUE NOT NULL,
    shortPercentage integer NOT NULL,
    shortPositions integer NOT NULL,
    shortVolume numeric  NOT NULL,
    shortAvgPrice numeric  NOT NULL,
    longPercentage integer NOT NULL,
    longPositions integer NOT NULL,
    longVolume numeric  NOT NULL,
    longAvgPrice numeric  NOT NULL,
    totalPositions integer NOT NULL
)

    """)

cur.close()

con.commit()
con.close()
