from flask import Flask, render_template
import pandas as pd
import numpy as np
import yfinance as yf
import requests
import json
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
