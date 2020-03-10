import os
import zipfile
import csv
import psycopg2
from datetime import datetime, timedelta
import shutil

columns_options = ["DISSEMINATION_ID", "ORIGINAL_DISSEMINATION_ID", "ACTION", "EXECUTION_TIMESTAMP", "CLEARED",
                   "EFFECTIVE_DATE", "END_DATE", "SETTLEMENT_CURRENCY", "TAXONOMY",
                   "PRICE_NOTATION_TYPE", "PRICE_NOTATION", "ADDITIONAL_PRICE_NOTATION", "NOTIONAL_CURRENCY_1",
                   "NOTIONAL_CURRENCY_2", "ROUNDED_NOTIONAL_AMOUNT_1", "ROUNDED_NOTIONAL_AMOUNT_2",
                   "EMBEDED_OPTION", "OPTION_STRIKE_PRICE", "OPTION_TYPE", "OPTION_CURRENCY", "OPTION_PREMIUM",
                   "OPTION_EXPIRATION_DATE", "PRICE_NOTATION2", "PRICE_NOTATION3"]

columns_NDF = ["DISSEMINATION_ID", "ORIGINAL_DISSEMINATION_ID", "ACTION", "EXECUTION_TIMESTAMP", "CLEARED",
               "EFFECTIVE_DATE", "END_DATE", "SETTLEMENT_CURRENCY", "TAXONOMY",
               "PRICE_NOTATION_TYPE", "PRICE_FORMING_CONTINUATION_DATA", "PRICE_NOTATION", "ADDITIONAL_PRICE_NOTATION_TYPE", "ADDITIONAL_PRICE_NOTATION",
               "NOTIONAL_CURRENCY_1", "NOTIONAL_CURRENCY_2", "ROUNDED_NOTIONAL_AMOUNT_1", "ROUNDED_NOTIONAL_AMOUNT_2"]

currencies = ["EUR", "GBP", "USD", "JPY", "CHF", "NZD", "AUD", "CAD"]


def unzip_all():
    for f in os.listdir("./Nezpracovano"):
        if ".zip" not in f[-4:]:
            continue
        if f in os.listdir("./ZpracovanoZIP"):
            continue

        with zipfile.ZipFile("./Nezpracovano/" + f, 'r') as zip_ref:
            zip_ref.extractall("ZpracovanoCSV")


def read_csv(filename):
    data = []
    with open(filename) as f:
        csv_dict = [{k: str(v) for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]

        for i in csv_dict:
            if "NDF" in i["TAXONOMY"]:
                if i["NOTIONAL_CURRENCY_1"] in currencies and i["NOTIONAL_CURRENCY_2"] in currencies:
                    rows_list = []
                    for col in columns_NDF:
                        if i[col] is "":
                            i[col] = None
                        if i[col] is not None and "," in i[col]:
                            i[col] = i[col].replace(",", "")
                            i[col] = i[col].replace("+", "")
                        rows_list.append(i[col])
                    data.append(tuple(rows_list))
    return data


def insert_data(data, filename):
    con = psycopg2.connect(
        host="<IP...>",
        database="<DBNAME>",
        user="<ADMINNAME>",
        password="<PASSWORD>"
    )
    cur = con.cursor()

    try:
        columns_string = ""
        for col in columns_NDF:
            columns_string = columns_string + col + ", "

        sql_insert_query = \
            f""" INSERT INTO NDF ({columns_string[:-2]})
                    VALUES (%s,%s,%s,TIMESTAMP %s,%s,TIMESTAMP %s,TIMESTAMP %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        for tup in data:
            cur.execute(sql_insert_query, tup)
            con.commit()
    except psycopg2.errors.UniqueViolation as e:
        print("Already inserted")
    finally:
        cur.close()
        con.close()

    curr_time = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    print("New data from SDR - %s - inserted at: %s" % (filename, curr_time))


def insert_all_csvs():
    path = "./ZpracovanoCSV/"
    for f in os.listdir(path):
        csv_data = read_csv(path + f)
        insert_data(csv_data, f)
        delete_csv(f)


def delete_csv(filename):
    os.remove("./ZpracovanoCSV/" + filename)
    zip_name = "CUMULATIVE_" + filename[:-4] + ".zip"
    if zip_name in os.listdir("./Nezpracovano"):
        shutil.move("./Nezpracovano/" + zip_name, "./ZpracovanoZIP")


if __name__ == '__main__':
    unzip_all()
    insert_all_csvs()
