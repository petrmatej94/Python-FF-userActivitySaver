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


pairs = ["NDF"]

columns_NDF = ["DISSEMINATION_ID", "ORIGINAL_DISSEMINATION_ID", "ACTION", "EXECUTION_TIMESTAMP", "CLEARED",
               "EFFECTIVE_DATE", "END_DATE", "SETTLEMENT_CURRENCY", "TAXONOMY",
               "PRICE_NOTATION_TYPE", "PRICE_FORMING_CONTINUATION_DATA", "PRICE_NOTATION", "ADDITIONAL_PRICE_NOTATION_TYPE", "ADDITIONAL_PRICE_NOTATION",
               "NOTIONAL_CURRENCY_1", "NOTIONAL_CURRENCY_2", "ROUNDED_NOTIONAL_AMOUNT_1", "ROUNDED_NOTIONAL_AMOUNT_2"]

cur = con.cursor()

for pair in pairs:
    cur.execute(f"""
    
CREATE TABLE {pair} (
    DISSEMINATION_ID numeric PRIMARY KEY,
    ORIGINAL_DISSEMINATION_ID numeric,
    ACTION VARCHAR(10) NOT NULL,
    EXECUTION_TIMESTAMP timestamp NOT NULL,
    CLEARED VARCHAR(5) NOT NULL,
    EFFECTIVE_DATE timestamp NOT NULL,
    END_DATE timestamp NOT NULL,
    SETTLEMENT_CURRENCY VARCHAR(5),
    TAXONOMY VARCHAR(20) NOT NULL,
    PRICE_NOTATION_TYPE VARCHAR(20) NOT NULL,
    PRICE_FORMING_CONTINUATION_DATA VARCHAR(20) NOT NULL,
    PRICE_NOTATION numeric NOT NULL,
    ADDITIONAL_PRICE_NOTATION_TYPE VARCHAR(15),
    ADDITIONAL_PRICE_NOTATION numeric,
    NOTIONAL_CURRENCY_1 VARCHAR(5) NOT NULL,
    NOTIONAL_CURRENCY_2 VARCHAR(5) NOT NULL,
    ROUNDED_NOTIONAL_AMOUNT_1 numeric NOT NULL,
    ROUNDED_NOTIONAL_AMOUNT_2 numeric NOT NULL
)

    """)

cur.close()

con.commit()
con.close()
