import os
from flask import Flask, render_template
import pandas as pd
import yfinance as yf
import requests
import json
import google.generativeai as palm

app = Flask(__name__, static_folder="static", template_folder="views")
FMP_API_KEY = os.environ.get("FMP_API_KEY")
GOOGLE_PALM_API_KEY = os.environ.get("google_palm_api_key")
symbol = "AAPL"
FMP_ENDPOINT = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?period=annual&apikey={FMP_API_KEY}"


@app.route("/")
def home():
    return render_template("index.html")
