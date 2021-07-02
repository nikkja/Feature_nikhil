from flask import Flask, render_template, request, jsonify
import sqlite3 as sq
import requests
import logging 
import pandas as pd
import json
app = Flask(__name__)
@app.route('/',methods = ['POST', 'GET'])
def details_company_date():
    if request.method == 'POST':
        try:
            company_name = request.form.get('name') #fetched the company name from the user.
            date = request.form.get('date')         #fetched the date from the user.
            with sq.connect('stock_data.db') as conn:
                cur = conn.cursor()
                #fetched the record from the table for the given company name and date 
                cur.execute("SELECT OPEN, HIGH, LOW, CLOSE from STOCK_PRICE WHERE COMPANY_NAME=? AND DATES=?", (company_name,date,))
                row = cur.fetchall()

            field = ['Open', 'High', 'Low', 'Close']
            df = pd.DataFrame(row, columns = field)
            df.to_csv('Output.csv', index=False)  #written the output to the CSV file
            
            res = {field[i]: row[0][i] for i in range(4)}
            result = json.dumps(res, indent=2)
            with open("Output.json","w") as j:
                j.write(result)                   #written the output to the JSON file

            return jsonify(res)
            #return render_template("details_company_date.html", result = res)
        except:
            logging.exception("ERROR IN RETRIVING")
            
    return render_template("details_company_date.html")

if __name__ == "__main__":
	app.run(debug=True)
