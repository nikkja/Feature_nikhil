from flask import Flask, render_template, request, jsonify
import sqlite3
import requests
import logging 
import pandas as pd
import json

# Flask constructor
app = Flask(__name__)

logging.basicConfig(filename='geo.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

def fun_create_table(): #function to create the table 
    conn = sqlite3.connect('stock_data.db')  #Opens a connections to the SQLite database file.

    logging.info("SUCCESSFULLY OPENED THE DATABASE")
    conn.execute('''CREATE TABLE IF NOT EXISTS STOCK_PRICE
         (COMPANY_NAME      VARCHAR(10)  NOT NULL,
         DATES              TEXT       NOT NULL,
         OPEN               REAL,
         HIGH               REAL,
         LOW                REAL,
         CLOSE              REAL,
         ADJUSTED_CLOSE     REAL,
         VOLUME             INT,
         DIVIDEND_AMOUNT    REAL,
         SPLIT_COEFFICIENT  REAL);''')  #Execute the sql statement
    logging.info("TABLE CREATED")
    conn.close()


def fun_data_entry(): #function to insert records in the table 
    conn = sqlite3.connect('stock_data.db')  #Opens a connections to the SQLite database file.

    logging.info("DATABASE OPENED")

    companys = ['MSFT', 'ABB', 'AAL', 'AAPL', 'DELL']    #list of the companys 
    try:
        for company in companys:
            #Extracted the data of companys using the API
            response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&apikey=NQCFKOVGZASY3EZ9&symbol={company}").json() 
            dates = response['Time Series (Daily)']
            for date in dates:
                values = [company, date]
                for v in dates[date].values(): 
                    values.append(v)            #records to be inserted in the table
                conn.execute("INSERT INTO STOCK_PRICE (COMPANY_NAME,DATES,OPEN,HIGH,LOW,CLOSE,ADJUSTED_CLOSE,VOLUME,DIVIDEND_AMOUNT,SPLIT_COEFFICIENT) VALUES (?,?,?,?,?,?,?,?,?,?)", values )
            conn.commit()       #commit our transaction
        logging.info("RECORDS ARE HERE")
        conn.close()  # Closes the database connection
    except Exception as e:
        logging.exception(str(e))


@app.before_first_request
def before_request(): #This function will run once before the first request to this instance of the application.
    fun_create_table() #creation of the table 
    fun_data_entry() #insertion in the table

if __name__ == "__main__":
	app.run(debug=True)