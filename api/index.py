from flask import Flask, render_template
import pandas as pd
import numpy as np
import yfinance as yf
import requests
import json
import pandas_datareader.data as web
import statsmodels.api as sm

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
