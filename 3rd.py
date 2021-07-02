from flask import Flask, render_template, request, jsonify
import sqlite3 as sq
import requests
import logging 
import pandas as pd
import json
app = Flask(__name__)

@app.route('/per_date_average')
def per_date_average():
    companys = ['MSFT', 'ABB', 'AAL', 'AAPL', 'DELL']    #list of the companys
    try:
        conn = sq.connect('stock_data.db')
        cur = conn.cursor()
        res = {}
        dates = []
        f = 1
        for company_name in companys:
            #fetched the record from the table for the given company name 
            cur.execute("SELECT OPEN, CLOSE, DATES from STOCK_PRICE WHERE COMPANY_NAME=?", (company_name,))
            row = cur.fetchall()

            temp=[]
            for i in range(len(row)):
                temp.append(row[i][0]-row[i][1])         #Calculating the difference between closing and opening value of a given company
                if f:
                    dates.append(row[i][2])       
            res[company_name] =  temp
            f = 0

        result = {}
        df = pd.DataFrame(res)
        temp = df.mean(axis = 1).tolist()           #calculating per date average of all companies 
        result = {dates[i]: float("{:.4f}".format(temp[i])) for i in range(len(dates))}
        conn.close()
    except:
        logging.exception("ERROR IN RETRIVING")
            
    return jsonify(result)
    #return render_template("per_date_average.html", result = result)
if __name__ == "__main__":
	app.run(debug=True)
