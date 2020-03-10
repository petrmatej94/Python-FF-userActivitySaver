import psycopg2
import ast
from datetime import datetime

# Script pro insert dat z txt souboru do DB


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
    print("Inserting %s" % pair)
    list_of_tuples = []
    sql_insert_query = f""" INSERT INTO {pair} (date, shortPercentage, shortPositions, shortVolume, shortAvgPrice, longPercentage, longPositions, longVolume, longAvgPrice, totalPositions) 
                               VALUES (TIMESTAMP %s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """

    with open('Symbols/%s.txt' % pair, 'r') as file:
        for line in file.readlines():
            json = ast.literal_eval(line)
            time = str(json['time']).replace(".", "-")

            tup = (time, json['shortPercentage'], json['shortPositions'], json['shortVolume'], json['avgShortPrice'],
                json['longPercentage'], json['longPositions'], json['longVolume'], json['avgLongPrice'],
                json['totalPositions'])

            if tup not in list_of_tuples:
                list_of_tuples.append(tup)

    cur.executemany(sql_insert_query, list_of_tuples)
    con.commit()
    print("Finished %s\n\n" % pair)



cur.close()

con.commit()
con.close()