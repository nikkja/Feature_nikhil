from flask import Flask, render_template, request, jsonify
import sqlite3 as sq
import requests
import logging 
import pandas as pd
import json
app = Flask(__name__)
@app.route('/per_date_difference',methods = ['POST', 'GET'])
def per_date_difference():
    if request.method == 'POST':
        try:
            company_name = request.form.get('name') #fetched the company name from the user.
            with sq.connect('stock_data.db') as conn:
                cur = conn.cursor()
                #fetched the record from the table for the given company name 
                cur.execute("SELECT OPEN, CLOSE, DATES from STOCK_PRICE WHERE COMPANY_NAME=?", (company_name,))
                row = cur.fetchall()

            res={}
            for i in range(len(row)):
                res[row[i][2]] = float("{:.4f}".format(row[i][0]-row[i][1]))        #Calculating the difference between closing and opening value of a given company
            #return render_template("per_date_difference.html", result = res)
            return jsonify(res)
        except:
            logging.exception("ERROR IN RETRIVING")
            
    return render_template("per_date_difference.html")

if __name__ == "__main__":
	app.run(debug=True)
