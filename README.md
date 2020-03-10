# Description of scripts

## ForexFactory-UserActivityDownloader.py
- This script was created because of user I was following was deleting his forum posts and sometimes I missed them. It goes through all his new posts and saves them to separate file.
- Selenium was used for automation of going through all new posts and saving HTML

## TesseractOCR-ImageReader.py
- There is a site which publish data tables in image format. I found tool for parsing image into text - Tesseract OCR. It parsed image into text file. This file contained a lot of white spaces and unrequired signs which I then removed and saved into CSV for data research. I also used data from CSV in another script (simple C++) which showed levels on the chart of trading terminal MetaTrader 4.

## FxBook-APIDataDownloader.py
- This script was used to automatically download data from API every minute, not including weekends. Script was running on my Linux server. I used Schedule library to run script every minute. It downloaded data and inserted them into PostgreSQL database. Any error with connection was logged into error log.

## FxBook-InsertDataToPostgres.py
- Needed to insert some historical data from text file into DB.

## FxBook-CreateTables.py
- Loop for creating all 28 tables

## UnzipCSVs-InsertToPostgreDB.py
- There was a website providing data from markets in CSV files. I needed to filter out some data and insert them into PostgreSQL database. I usually downloaded a lot of files, so I needed program which goes through all of them at once.
## UnzipCSVs-CreateTablesScript.py
- Script for creating table. Actually this SQL I could make directly in SQL, not in Python.

