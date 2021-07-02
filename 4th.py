from flask import Flask, render_template, request, jsonify
import sqlite3 as sq
import requests
import logging 
import pandas as pd
import json
app = Flask(__name__)

@app.route('/number_of_continuous_days',methods = ['POST', 'GET'])
def number_of_continuous_days():
    if request.method == 'POST':
        try:
            company_name = request.form.get('name') #fetched the company name from the user.
            with sq.connect('stock_data.db') as conn:
                cur = conn.cursor()
                #fetched the record from the table for the given company name 
                cur.execute("SELECT OPEN, CLOSE, DATES from STOCK_PRICE WHERE COMPANY_NAME=?", (company_name,))
                row = cur.fetchall()

            result={}
            temp = 0
            maximum_days = 0
            temp1 = []
            dates = []
            for i in range(len(row)):
                if row[i][0] < row[i][1]:       #Checking that the closing value is greater than opening value
                    temp1.append(row[i][2])
                    temp+=1                     #count of continuous days with closing value is greater than opening value
                else:
                    if maximum_days < temp:                #checking whether it is maximum number of continuous days or not
                        maximum_days = temp
                        dates = temp1
                    temp1 = [] 
                    temp = 0
            result[maximum_days] = dates
            return jsonify(result)
            #return render_template("number_of_continuous_days.html", result = result)
        except:
            logging.exception("ERROR IN RETRIVING")
            
    return render_template("number_of_continuous_days.html")
if __name__ == "__main__":
	app.run(debug=True)
