import time

import psycopg2
import requests
import schedule
from datetime import datetime, timedelta

# API URL
login_url = 'https://www.myfxbook.com/api/login.json?email=<EMAIL>&password=<PASSWORD>'
pairs = ["EURUSD", "GBPUSD", "USDCHF", "AUDUSD", "NZDUSD", "USDCAD", "USDJPY",
         "EURGBP", "GBPCHF", "GBPAUD", "GBPNZD", "GBPCAD", "GBPJPY",
         "EURCHF", "EURAUD", "EURNZD", "EURCAD", "EURJPY",
         "AUDCHF", "NZDCHF", "CADCHF", "CHFJPY",
         "AUDCAD", "NZDCAD", "CADJPY",
         "AUDNZD", "NZDJPY",
         "AUDJPY"]




def login():
    error = True
    response_json = None

    while error is True:
        try:
            response = requests.get(login_url)
            response_json = response.json()
            error = response_json['error']
        except Exception as ex:
            error = True
            print("Error during login: %s. Waiting 5s until next request" % ex)
            time.sleep(5)

    return response_json['session']


def get_outlook():
    error = True
    response_json = None

    while error is True:
        try:
            session = login()
            response = requests.get('http://www.myfxbook.com/api/get-community-outlook.json?session=%s' % session)
            response_json = response.json()
            error = response_json['error']
        except Exception as e:
            error = True
            print("Error at getting data: %s. Waiting 5s until next request" % e)
            time.sleep(5)

    return response_json


def job():
    now = datetime.now() - timedelta(hours=2)
    if now.strftime("%A") in ['Saturday', 'Sunday']:
        print("It's weekend, no data fetched")
    else:
        curr_time = datetime.now().strftime('%Y.%m.%d %H:%M:%S')

        outlook = get_outlook()
        symbols = outlook['symbols']

        con = psycopg2.connect(
            host="<IP...>",
            database="<DBNAME>",
            user="<ADMINNAME>",
            password="<PASSWORD>"
        )
        cur = con.cursor()

        for symbol in symbols:
            if symbol['name'] in pairs:
                symbol['time'] = curr_time

                sql_insert_query = \
                    f""" INSERT INTO {symbol['name']} (date, shortPercentage, shortPositions, shortVolume, shortAvgPrice, longPercentage, longPositions, longVolume, longAvgPrice, totalPositions) 
                    VALUES (TIMESTAMP %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

                record_to_insert = (
                    curr_time, symbol['shortPercentage'], symbol['shortPositions'], symbol['shortVolume'], symbol['avgShortPrice'],
                    symbol['longPercentage'], symbol['longPositions'], symbol['longVolume'], symbol['avgLongPrice'], symbol['totalPositions']
                )

                cur.execute(sql_insert_query, record_to_insert)
                con.commit()

                # with open('Symbols/%s.txt' % symbol['name'], 'a+') as file:
                #     file.write('%s\n' % (str(symbol)))

        cur.close()
        con.close()
        print("New data fetched at: " + curr_time)


if __name__ == '__main__':
    schedule.every().minute.at(":00").do(job)

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("Interrupted by keyboard")
            break
        except Exception as e:
            print("Error found: ", e)
            with open('errorlog.txt', 'a+') as file:
                file.write("%s --- %s \n'" % (datetime.now(), e))
            schedule.run_pending()
            time.sleep(1)
